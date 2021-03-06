# encoding: utf-8
"""
@author:  sherlock
@contact: sherlockliao01@gmail.com
"""

import glob
import re
import numpy as np

import os.path as osp

from .bases import BaseImageDataset


class CUHK03_D(BaseImageDataset):
	"""
        cuhk03-np detected
	"""
	dataset_dir = 'cuhk03-np/detected'
	__name__ = 'cuhk03_d'

	def __init__(self, root='/mnt/lustre/reid/data', verbose=True, **kwargs):
		super(CUHK03_D, self).__init__()
		self.dataset_dir = osp.join(root, self.dataset_dir)
		self.train_dir = osp.join(self.dataset_dir, 'train.txt')
		self.query_dir = osp.join(self.dataset_dir, 'test_probe.txt')
		self.gallery_dir = osp.join(self.dataset_dir, 'test_gallery.txt')

		self._check_before_run()

		train = self._process_train(self.train_dir, self.dataset_dir)
		query = self._process_probe(self.query_dir, self.dataset_dir)
		gallery = self._process_gallery(self.gallery_dir, self.dataset_dir)

		if verbose:
			print("=> CUHK03 Detected loaded")
			self.print_dataset_statistics(train, query, gallery)

		self.num_train_pids, self.num_train_imgs, self.num_train_cams = self.get_imagedata_info(train)
		self.num_query_pids, self.num_query_imgs, self.num_query_cams = self.get_imagedata_info(query)
		self.num_gallery_pids, self.num_gallery_imgs, self.num_gallery_cams = self.get_imagedata_info(gallery)

		self.train = train
		self.query = query
		self.gallery = gallery

	def _check_before_run(self):
		"""Check if all files are available before going deeper"""
		if not osp.exists(self.dataset_dir):
			raise RuntimeError("'{}' is not available".format(self.dataset_dir))
		if not osp.exists(self.train_dir):
			raise RuntimeError("'{}' is not available".format(self.train_dir))
		if not osp.exists(self.query_dir):
			raise RuntimeError("'{}' is not available".format(self.query_dir))
		if not osp.exists(self.gallery_dir):
			raise RuntimeError("'{}' is not available".format(self.gallery_dir))

	def _process_train(self, train_list, root):
		id_tracker = {}
		id_cnt = 0
		dataset = []
		with open(train_list, 'r') as f:
			lines = f.readlines()
			for l in lines:
				l = l.strip().split()
				img_path, pid = l[0], l[1]
				# relabel 
				if pid not in id_tracker:
					id_tracker[pid] = id_cnt
					pid = id_cnt
					id_cnt += 1
				else:
					pid = id_tracker[pid]
				#camid = img_path.split('/')[1].split('_')[2]
				dataset.append((osp.join(root, img_path), pid, 0)) #train cam treated as the same
		return dataset

	def _process_probe(self, test_list, root):
		cam = np.load('/mnt/lustre/liuyuan1/cvpr20/data/cuhk03-np/detected/cam_probe.npy')
		dataset = []
		with open(test_list, 'r') as f:
			lines = f.readlines()
			for i, l in enumerate(lines):
				l = l.strip().split()
				img_path, pid = l[0], l[1]
				camid = cam[i] #img_path.split('/')[1].split('_')[2]
				dataset.append((osp.join(root, img_path), int(pid), int(camid)-1))
		return dataset

	def _process_gallery(self, test_list, root):
		cam = np.load('/mnt/lustre/liuyuan1/cvpr20/data/cuhk03-np/detected/cam_gallery.npy')
		dataset = []
		with open(test_list, 'r') as f:
			lines = f.readlines()
			for i, l in enumerate(lines):
				l = l.strip().split()
				img_path, pid = l[0], l[1]
				camid = cam[i] #img_path.split('/')[1].split('_')[2]
				dataset.append((osp.join(root, img_path), int(pid), int(camid)-1))
		return dataset
