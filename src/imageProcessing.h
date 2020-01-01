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
};
