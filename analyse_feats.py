import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os
from tqdm import tqdm
import pickle
import argparse

class FeatureAnalysis():

    def __init__(self, path, keep, server=True):

        self.parent_path = path
        self.frame_list = self.get_paths(keep_files=keep)
        
        self.all_feat_frame = self.create_dataframe()

    def run(self, k):

        self.k = k
        self.kmeans = self.calc_kmeans()
        self.plot_kmeans()
        self.save_model(self.kmeans)

    def save_model(self, model):

        model_name = "kmeans.pkl"

        with open(model_name, "wb") as f:
            pickle.dump(model, f)


    def get_paths(self, keep_files=0):

        frame_list = []
        for folder in os.listdir(self.parent_path):
            feat_frame = os.path.join(self.parent_path, os.path.join(folder, "features_frame.csv"))
            print(feat_frame)
            if os.path.isfile(feat_frame):
                frame_list.append(feat_frame)

        if keep_files > 0:
            print("Reducing feature files from: {0} to: {1}".format(len(frame_list), keep_files))
            frame_list = frame_list[:keep_files]

        return frame_list


    def create_dataframe(self):

        all_feat_frame = pd.DataFrame([])
        print("Getting features...")
        for frame_file in tqdm(self.frame_list):
            frame = pd.read_csv(frame_file)
            all_feat_frame = pd.concat([all_feat_frame, frame])

        print("Features Shape: (patches, fileName + features)", all_feat_frame.values.shape)

        return all_feat_frame

    def check_kmeans(self, data, paths):

        res = list()
        n_cluster = range(20,500,20)

        for n in n_cluster:
            print("Checking for {0} Clusters...".format(n))
            kmeans = KMeans(n_clusters=n)
            kmeans.fit(data)
            res.append(kmeans.inertia_)

        plt.plot(n_cluster, res)
        plt.title('elbow curve')
        plt.savefig("elbow_curve.png")
        # plt.show()

        return 2

    def calc_kmeans(self):
        self.data = self.all_feat_frame.iloc[:, 1:].values
        self.paths = [d[0] for d in self.all_feat_frame.iloc[:, :1].values]

        kmeans = KMeans(n_clusters=self.k, random_state=0).fit(self.data)

        return kmeans

    def plot_kmeans(self):

        centroids = self.kmeans.cluster_centers_
        # print(centroids)
        dirname = "{0}_clusters".format(self.k)

        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        for n, center in enumerate(centroids):
            fig, ax = plt.subplots(3,3)
            
            distances = np.argsort(np.linalg.norm(self.data - center, axis=1))
            cen = distances[0]
            fig.suptitle("Center: {0} | Patch: {1}".format(n, self.paths[cen]))

            for ind, a in enumerate(ax.flatten()):
                dist = distances[ind]
                # print(paths[dist])
                with Image.open(self.paths[dist]) as im:
                    patch_img = im.copy()


                a.imshow(patch_img)
                a.axis("off")
            # ax[int(n%3), n].imshow(patch_img)

            plt.savefig(os.path.join(dirname, "cluster_{0}.png".format(n)))

            # plt.show()

        

    def check_on_server(self):

        csv_path = "/home/simon/philipp/docker/features_frame.csv"
        data_ = pd.read_csv(csv_path)
        data = data_.iloc[:, 1:].values
        paths = [d[0] for d in data_.iloc[:, :1].values]
        # print(paths)
        # print(data)
        # k = check_kmeans(data, paths)

        kmeans_plot(data, paths)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--k_clusters', required=False, nargs='+', default=[200])
    parser.add_argument('-ke', '--keep', type=int, required=False, default=0)
    args = parser.parse_args()

    k_clusters = args.k_clusters
    keep = args.keep

    # print(k_clusters)

    path = "/home/simon/philipp/patches"
    fa = FeatureAnalysis(path, keep=keep)
    for k in k_clusters:
        print("kmeans with: ", int(k))
        fa.run(int(k))


    # check_on_server()

    # patch_path = "/media/user/easystore/patches/"
    # patch_path_ = "/media/user/easystore/DigitalSlide_A1M_9S_1_20190127165819218/"
    # csv_path = "/home/user/Documents/Master/docker/features_frame.csv"
    # csv_path_low = "/home/user/Documents/Master/docker/features_frame_low_att.csv"


    # num_patches = -1

    # data_ = pd.read_csv(csv_path)
    # data = data_.iloc[:, 1:].values[:num_patches]

    # data_low_ = pd.read_csv(csv_path_low)
    # data_low = data_low_.iloc[:, 1:].values[:num_patches]

    # paths = [p[0].replace("/home/simon/philipp/", patch_path) for p in data_.iloc[:, :1].values]
    # paths_low = [p[0].replace("/home/simon/philipp/patches/", patch_path) for p in data_low_.iloc[:, :1].values]


    # all_data = np.concatenate((data[:num_patches], data_low[:num_patches]))
    # all_paths = np.concatenate((paths[:num_patches], paths_low[:num_patches]))


    # # k = check_kmeans(all_data, all_paths)
    # kmeans_plot(all_data, all_paths)
    