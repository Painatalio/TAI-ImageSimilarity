//
// Created by Pedro Ferreira,
//            Rafael Direito,
//            Rafael Teixeira.
//

#include <dirent.h>
#include <sys/stat.h>
#include "imageProcessing.h"

using namespace cv;


std::vector<std::string> openDir(const std::string& path){
    DIR*    dir;
    dirent* pdir;
    std::vector<std::string> files{};

    if (path.back() != '/' and path != ".") {
        std::cerr << "Directory is missing the / at the end!" << std::endl;
        exit(EXIT_FAILURE);
    }

    dir = opendir(path.c_str());

    if (dir == nullptr) {
        std::cerr << "Directory doesn't exist!" << std::endl;
        exit(EXIT_FAILURE);
    }

    while ((pdir = readdir(dir)))
        if (strncmp(pdir->d_name, ".", 1) != 0 and strncmp(pdir->d_name, "..", 2) != 0)
            files.emplace_back(pdir->d_name);

    return files;
}

void imageProcessing::quantize(const std::string& path, int q) {
    std::vector<std::string> images = openDir(path);
    std::string save_folder;
    size_t pos;
    std::string p(path);

    while ((pos = p.find('/')) != std::string::npos) {
        save_folder = p.substr(0, pos);
        p.erase(0, pos + 1);
    }

    std::string new_path = "../quant_faces/" + save_folder + "/";
    mkdir(new_path.c_str(), 0777);

    for (const auto& image : images) {
        Mat img = imread(path + image, CV_LOAD_IMAGE_GRAYSCALE);

        if (img.empty()) {
            std::cerr << "Couldn't open or find the image " << image << std::endl;
            std::cerr << "Do you want to continue? (y/n)" << std::endl;
            int key = std::cin.get();

            while (key != 'y' and key != 'n') {
                std::cin.clear();
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                std::cerr << "Choice must be y or n! Try again, please!" << std::endl;
                key = std::cin.get();
            }

            if (key == 'n')
                exit(EXIT_FAILURE);

            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        }

        for (auto it = img.begin<uchar>() ; it != img.end<uchar>() ; ++it)
            *it = (*it / q) * q + (q >> 1);

        imwrite(new_path + image, img);
    }
}

void imageProcessing::reduce_resolution() {

}

void imageProcessing::split_dataset() {

}

int main(int argc, char *argv[]) {
    imageProcessing ip;
    ip.quantize("../orl_faces/s01/", 128);
}