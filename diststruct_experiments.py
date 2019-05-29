#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import io
import sys
import numpy as np
import tensorflow as tf
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile
from gensim.models.keyedvectors import KeyedVectors
import itertools
from matplotlib import pyplot as plt
import matplotlib as mpl
import pandas as pd
import random
import seaborn as sns
from scipy.cluster import hierarchy
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import jaccard_similarity_score
from featurephone import phone_to_features
from scipy.stats import pearsonr, spearmanr, shapiro, normaltest, kstest
from scipy.spatial.distance import euclidean

mpl.rc('font', **{'sans-serif' : 'DejaVu Sans',
                         'family' : 'sans-serif'})
mpl.rc('legend', fontsize=11)

# Extract non-CMU word lists
def extract_wordlist(dictfile):
    prondict = []
    with io.open(dictfile,'r',encoding='utf-8') as f:
        for line in f:
            line = '# '+line
            prondict.append(line.strip('\n').split('\t')[0].split())
    
    return prondict

# Extract CMU dictionary
def extract_cmudictionary(dictfile):
    prondict = {}
    with io.open(dictfile, 'r') as f1:
        for line in f1:
            prondict[line.strip('\n').split('#')[0].split(' ')[0]] = line.strip('\n').split('#')[0].strip().split(' ')[1:]
            prondict[line.strip('\n').split('#')[0].split(' ')[0]].insert(0,'#')

    return prondict

def read_corpus(learn):
    if 'cmu' in learn:
        corpus = extract_cmudictionary(learn).values()
    else:
        corpus = extract_wordlist(learn)

    #Contolling the size of corpus
    #corpus1 = random.sample(list(corpus),4000)
    #corpus1 = list(corpus)[:4000]

    return corpus

#Change parameters based on experiments 
#Preliminary experiments (Silfverberg et al. 2018)- dim 30, negative=1, window=1, min_count=5
#Artificial language experiment- dim 30, negative=5, window=5, min_count=5
#English distributional phonology- dim 200, negative=5, window=5, min_count=5
def build_model(corpus):
    model = Word2Vec(corpus,size=30,workers=8,negative=5,window=3,alpha=0.05,min_count=5)
    model.wv.save_word2vec_format("phone-embeddings.txt",binary=False)

# Extract phonetic distances based on distinctive features
def extract_phonetic_distmatrix(featfile):
    model = KeyedVectors.load_word2vec_format('phone-embeddings.txt', binary=False)
    phon_vectors = model.wv
    feature_matrix = {}
    distmat = {}
    feat_lines = list(filter(None,open(featfile,'r').read().split('\n')))
    feat_labels = feat_lines[0].split()
    for l in feat_lines[1:]:
        feature_matrix[l.split()[0]] = []
        for f,v in zip(feat_labels,l.split()[1:]):
            if v == '+' or v == '-':
                feature_matrix[l.split()[0]].append(v+f)
    for k in feature_matrix.keys():
        print(k, feature_matrix[k])
    for p in list(itertools.product(phon_vectors.index2word,phon_vectors.index2word)):
        f1= set(feature_matrix[p[0]]) 
        f2 = set(feature_matrix[p[1]])
        distmat[(p[0],p[1])] = 1.0 - (float(len(f1 & f2)) / (len(f1) + len(f2) - len(f1 & f2)))
        #distmat[(p[0],p[1])] = float(len(f1 & f2)) / (len(f1) + len(f2) - len(f1 & f2))
    
    return distmat

# Extract phonetic distances for CMU based on Parrish (2017)
def extract_cmu_phonetic_distmatrix():
    model = KeyedVectors.load_word2vec_format('phone-embeddings.txt', binary=False)
    phon_vectors = model.wv
    distmat = {}
    for p in list(itertools.product(phon_vectors.index2word,phon_vectors.index2word)):
        f1= set(phone_to_features(p[0]))
        f2 = set(phone_to_features(p[1]))
        #distmat.setdefault(p[0],{})[p[1]] = jaccard_similarity_score(list(phone_to_features(p[0])),list(phone_to_features(p[1]))) 
        distmat[(p[0],p[1])] = 1.0 - (float(len(f1 & f2)) / (len(f1) + len(f2) - len(f1 & f2)))
        #distmat[(p[0],p[1])] = float(len(f1 & f2)) / (len(f1) + len(f2) - len(f1 & f2))
    
    return distmat

# PCA and t-SNE plots of embeddings
def visualize_embeddings():
    model = KeyedVectors.load_word2vec_format('phone-embeddings.txt', binary=False)
    X = model[model.wv.vocab]
    pca = PCA(n_components=2,svd_solver='auto',random_state=1000)
    #pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X)
    
    # create a scatter plot of the projection
    plt.scatter(pca_result[:, 0], pca_result[:, 1])
    words = list(model.wv.vocab)
    for i, word in enumerate(words):
        plt.annotate(word, xy=(pca_result[i, 0], pca_result[i, 1]),size=24)
        #plt.annotate(word, xy=(pca_result[i, 0], pca_result[i, 1]),size=10)
    plt.savefig('pcaplot.pdf')
    plt.close()

    #for ppl in range(1,11,1):
    #    for e in range(20,220,20):
    tsne = TSNE(n_components=2,perplexity=2.5,n_iter=5000, n_iter_without_progress=300, learning_rate=100,early_exaggeration=15.0)
    tsne_result = tsne.fit_transform(X)

    # create a scatter plot of the projection
    plt.scatter(tsne_result[:, 0], tsne_result[:, 1])
    words = list(model.wv.vocab)
    for i, word in enumerate(words):
        plt.annotate(word, xy=(tsne_result[i, 0], tsne_result[i, 1]),size=24)
        #plt.annotate(word, xy=(tsne_result[i, 0], tsne_result[i, 1]),size=10)
    plt.savefig('tsneplot-ppl2-eps100.pdf')
    plt.close()

# Extract distributional distances based on cosine similarity between embeddings
def extract_word2vec_distmatrix():
    model = KeyedVectors.load_word2vec_format('phone-embeddings.txt', binary=False)
    phon_vectors = model.wv
    distmat = {}
    for p in list(itertools.product(phon_vectors.index2word,phon_vectors.index2word)):
        #distmat.setdefault(p[0],{})[p[1]] = phon_vectors.similarity(p[0],p[1])
        distmat.setdefault(p[0],{})[p[1]] = euclidean(phon_vectors[p[0]],phon_vectors[p[1]])
        #distmat[(p[0],p[1])] = phon_vectors.similarity(p[0],p[1])
    
    return distmat


# Plot dendrogram clusters of phones
def plot_clusters():
    distmat = extract_word2vec_distmatrix()
    df = pd.DataFrame.from_dict(distmat)
    Z = hierarchy.linkage(df, 'average')
    plt.figure(figsize=(8, 5))
    hierarchy.dendrogram(Z, orientation='top', labels=df.index, leaf_font_size=18, leaf_rotation=0, distance_sort='descending', show_leaf_counts=False)
    #plt.title('Hierarchical Clustering Dendrogram')
    #plt.ylabel('Distance')
    #plt.xlabel('Phones')
    plt.savefig('phone-dendrogram.pdf')
    plt.close()

# Plot heatmap cluster
def plot_distmat():
    distmat = extract_word2vec_distmatrix()
    df = pd.DataFrame.from_dict(distmat)
    sns.set(font_scale = 2.0)
    #sns.set(font_scale = 0.65)
    cg = sns.clustermap(df, xticklabels=True, yticklabels=True, cmap="Spectral_r")
    #cg.ax_row_dendrogram.set_visible(False)
    plt.savefig('phone-heatmap.pdf')
    plt.close()

# analogies, odd one out tasks, inter-phone similarities to file
def evaluate_embeddings1():
    model = KeyedVectors.load_word2vec_format('phone-embeddings.txt', binary=False)
    phon_vectors = model.wv
    with open('eval1-embeddings','w') as f1:
        for c in list(itertools.permutations(phon_vectors.index2word, 3)):
            result = phon_vectors.most_similar(positive=[c[0], c[1]], negative=[c[2]])
            f1.write("Analogies - %s + %s - %s = %s\n"%(c[0],c[1],c[2],str("{}: {:.4f}".format(*result[0]))))
        #for c in list(itertools.permutations(phon_vectors.index2word, 5)):
        #    f1.write("Which one among these is the odd one out - / %s /?- %s\n"%(" ".join(c), str(phon_vectors.doesnt_match(c))))
        #distmat = extract_word2vec_distmatrix()
        #for k1 in distmat.keys():
        #    for k2 in distmat[k1].keys():
        #        f1.write("Similarity between %s and %s is %s\n"%(k1,k2,str(phon_vectors.similarity(k1,k2))))


# analogies among English vowels based on CMU arpabet transcription
def evaluate_embeddings2():
    model = KeyedVectors.load_word2vec_format('phone-embeddings.txt', binary=False)
    phon_vectors = model.wv
    with open('eval2-embeddings','w') as f1:
        for c1 in phon_vectors.index2word:
            if c1[0] in ['A','E','I','O','U']:
                for c2 in phon_vectors.index2word:
                    if c2[0] in ['A','E','I','O','U']:
                        for c3 in phon_vectors.index2word:
                            if c3[0] in ['A','E','I','O','U']:
                                f1.write("%s + %s - %s = %s\n"%(c1, c2, c3, str(phon_vectors.most_similar(positive=[c1, c2], negative=[c3], topn=1)[0][0])))
    
# correlation between distinctive feature space and embedding space
def get_correlation(learn,feat):
    if 'cmu' in learn:
        phonetic_distmat = extract_cmu_phonetic_distmatrix()
    else:
        phonetic_distmat = extract_phonetic_distmatrix(feat)
    word2vec_dist = extract_word2vec_distmatrix()
    word2vec_distmat = {}
    for k1 in word2vec_dist.keys():
        for k2 in word2vec_dist[k1]:
            word2vec_distmat[(k1,k2)] = word2vec_dist[k1][k2]
    print(sorted(phonetic_distmat)==sorted(word2vec_distmat))
    phonetic_distances = [phonetic_distmat[k] for k in sorted(phonetic_distmat)]
    distributional_distances = [word2vec_distmat[k] for k in sorted(phonetic_distmat)]
    print("Pearson correlation coefficient:",pearsonr(phonetic_distances, distributional_distances))
    print("Spearman correlation coefficient:",spearmanr(phonetic_distances, distributional_distances))
    stat, p = shapiro(phonetic_distances)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Phonetic Distances looks Gaussian (fail to reject H0)')
    else:
        print('Phonetic Distances does not look Gaussian (reject H0)')
    stat, p = shapiro(distributional_distances)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Distributional Distances looks Gaussian (fail to reject H0)')
    else:
        print('Distributional Distances does not look Gaussian (reject H0)')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--correlation",help="Correlation between phonetic similarity and word2vec similarity",action='store_true')
    parser.add_argument("--plotembeddings",help="PCA and t-SNE plots of embeddings",action='store_true')
    parser.add_argument("--dendrogram",help="Dendrogram plot of embeddings",action='store_true')
    parser.add_argument("--heatmap",help="Heat map of embeddings",action='store_true')
    parser.add_argument("--evalembeddings1",help="Evaluation of embeddings",action='store_true')
    parser.add_argument("--evalembeddings2",help="Evaluation of embeddings",action='store_true')
    parser.add_argument("--learningdata",help="Phonetic transcribed corpus file")
    parser.add_argument("--featuredata",help="Phonetic feature specification")
    args = parser.parse_args()
    corpus = read_corpus(args.learningdata)
    build_model(corpus)
    if args.correlation:
        get_correlation(args.learningdata,args.featuredata)
    if args.plotembeddings:
        visualize_embeddings()
    if args.heatmap:
        plot_distmat()
    if args.dendrogram:
        plot_clusters()
    if args.evalembeddings1:
        evaluate_embeddings1() 
    if args.evalembeddings2:
        evaluate_embeddings2() 

if __name__ == "__main__":
    main()
