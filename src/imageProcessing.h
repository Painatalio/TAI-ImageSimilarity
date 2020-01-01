//
// Created by Pedro Ferreira,
//            Rafael Direito,
//            Rafael Teixeira.
//

#include <ios>
#include <cstdio>
#include <string>
#include <fstream>
#include <iostream>
#include <dirent.h>
#include <sys/stat.h>
#include <opencv2/highgui/highgui.hpp>


class imageProcessing {
public:
    static void quantize(const std::string& path, int q);

    static void reduce_resolution(const std::string& path, int width, int height);

    static void split_dataset(const std::string& path, int images_per_subject);

    static void live_face_recognition(int deviceID, int apiID);

    static void take_pictures(int deviceID, int apiID, int num_pictures, const std::string& name_prefix, const std::string& save_path);
};
