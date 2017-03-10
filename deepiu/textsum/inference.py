#!/usr/bin/env python
# -*- coding: gbk -*-
# ==============================================================================
#          \file   predict.py
#        \author   chenghuige  
#          \date   2016-10-19 06:54:26.594835
#   \Description  
# ==============================================================================

  
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
flags = tf.app.flags
FLAGS = flags.FLAGS

#FIXME: attention will hang..., no attention works fine
#flags.DEFINE_string('model_dir', '/home/gezi/temp/textsum/model.seq2seq.attention/', '')
flags.DEFINE_string('model_dir', '/home/gezi/temp/textsum/model.seq2seq/', '')
flags.DEFINE_string('vocab', '/home/gezi/temp/textsum/tfrecord/seq-basic.10w/train/vocab.txt', 'vocabulary file')
flags.DEFINE_boolean('pad', True, 'wether to pad to pad 0 to make fixed length text ids')

import sys, os
import gezi, melt
import numpy as np

from deepiu.util import text2ids

import conf  
from conf import TEXT_MAX_WORDS, INPUT_TEXT_MAX_WORDS, NUM_RESERVED_IDS, ENCODE_UNK

#TODO: now copy from prpare/gen-records.py
def _text2ids(text, max_words):
  word_ids = text2ids.text2ids(text, seg_method=FLAGS.seg_method, feed_single=FLAGS.feed_single, allow_all_zero=True, pad=False)
  word_ids_length = len(word_ids)

  if len(word_ids) == 0:
    return []
  word_ids = word_ids[:max_words]
  if FLAGS.pad:
    word_ids = gezi.pad(word_ids, max_words, 0)

  return word_ids

def predict(predictor, input_text):
  #TODO: why hang...
  word_ids = _text2ids(input_text, INPUT_TEXT_MAX_WORDS)
  print('word_ids', word_ids)
  print(text2ids.ids2text(word_ids))

  timer = gezi.Timer()
  text, score = predictor.inference(['text', 'text_score'], 
                                    feed_dict= {
                                      'seq2seq/model_init_1/input_text:0': [word_ids]
                                      })
  
  for result in text:
    print(result, text2ids.ids2text(result), timer.elapsed())
  
  timer = gezi.Timer()
  texts, scores = predictor.inference(['beam_text', 'beam_text_score'], 
                                    feed_dict= {
                                      'seq2seq/model_init_1/input_text:0': [word_ids]
                                      })

  texts = texts[0]
  scores = scores[0]
  for text, score in zip(texts, scores):
    print(text, text2ids.ids2text(text), score, timer.elapsed())

def main(_):
  text2ids.init()
  predictor = melt.Predictor(FLAGS.model_dir)
  predict(predictor, "王凯整容了吗_王凯整容前后对比照片")
  predict(predictor, "任达华传授刘德华女儿经 赞停工陪太太(图)")
  predict(predictor, "大小通吃汉白玉霸王貔貅摆件 正品开光镇宅招财")
  predict(predictor, "学生迟到遭老师打 扇耳光揪头发把头往墙撞致3人住院")

if __name__ == '__main__':
  tf.app.run()
