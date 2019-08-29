#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import cv_bridge
from datetime import datetime
import os
import rospy
import sys

from picam_ros.msg import picam_photo

###############################################################################
# Global Variable
GV_cv_bridge = cv_bridge.CvBridge()

###############################################################################
#
def save_photo(msg):

    print("[INFO] Call : save_photo")
    print("[INFO] msg.timestamp=%s" % msg.timestamp)
    dt = datetime.fromtimestamp(msg.timestamp.secs)

    #
    dir_data = "%s/photo/%04d/%02d" % (os.environ['PICAM_DATA'], dt.year, dt.month)
    if (not os.path.exists(dir_data)):
        os.makedirs(dir_data)

    #
    dt_str = "%04d%02d%02dT%02d%02d%02d" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    filename_base = "%s/%s-%s" % (dir_data, dt_str, msg.edge_id)

    # save meta
    filename_meta = filename_base + ".meta"
    with open(filename_meta, mode='w') as fh:
        fh.write("%s\t%s\n" % ( "date"           , dt_str) )
        fh.write("%s\t%s\n" % ( "edge_id"        , msg.edge_id ) )
        fh.write("%s\t%s\n" % ( "photo.height"   , str(msg.picam_photo.height) ) )
        fh.write("%s\t%s\n" % ( "photo.width"    , str(msg.picam_photo.width) ) )
        fh.write("%s\t%s\n" % ( "photo.encoding" , msg.picam_photo.encoding ) )

    # Convert ros photo data to cv2 photo data
    photo_cv2 = GV_cv_bridge.imgmsg_to_cv2(msg.picam_photo, desired_encoding="passthrough")

    # do somethins(resize/mask/filter/etc.)

    # save photo
    filename_photo = filename_base + ".jpg"
    cv2.imwrite(filename_photo, photo_cv2)

###############################################################################
#
def sub_photo():
    rospy.init_node('sub_photo', anonymous=True)
    rospy.Subscriber('example_picam_photo', picam_photo, save_photo)
    rospy.spin()

###############################################################################
#
if (__name__ == '__main__'):
    sub_photo()

# eof
