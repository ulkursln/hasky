source ./config 

python ./inference.py \
      --seg_method $online_seg_method \
      --feed_single $feed_single 
