//
// Created by Pedro Ferreira,
//            Rafael Direito,
//            Rafael Teixeira.
//

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

std::string newPath(const std::string& path, const std::string& initial_path, bool create_folder) {
    size_t pos;
    std::string p(path);
    std::string save_folder;

    while ((pos = p.find('/')) != std::string::npos) {
        save_folder = p.substr(0, pos);
        p.erase(0, pos + 1);
    }

    std::string new_path = initial_path + save_folder + "/";

    if (create_folder)
        mkdir(new_path.c_str(), 0777);

    return new_path;
}

void imageProcessing::quantize(const std::string& path, int q) {
    std::string initial_path = "../quant_faces/";
    std::string new_path = newPath(path, initial_path, true);
    std::vector<std::string> images = openDir(path);

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

void imageProcessing::reduce_resolution(const std::string& path, int width, int height) {
    std::string initial_path = "../reduced_faces/";
    std::string new_path = newPath(path, initial_path, true);
    std::vector<std::string> images = openDir(path);

    for (const auto& image : images) {
        Mat img = imread(path + image, CV_LOAD_IMAGE_GRAYSCALE);
        Mat dst(height, width, img.depth());

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

        IplImage tmp = img;
        IplImage iplDst = dst;
        cvResize(&tmp, &iplDst, CV_INTER_AREA);
        imwrite(new_path + image, dst);
    }
}

void imageProcessing::split_dataset(const std::string& path, int images_per_subject) {
    std::string reference_path = newPath(path, "../reference_subset/", false);
    reference_path = reference_path.substr(0, reference_path.size() - 1);
    std::string test_path = newPath(path, "../test_subset/", false);
    test_path = test_path.substr(0, test_path.size() - 1);
    std::vector<std::string> images = openDir(path);

    if (images_per_subject >= images.size()) {
        std::cerr << "ERROR: All images were requested for the reference subset, "
                     "or the requested number of images for the reference subset "
                     "is greater than the number of available images!" << std::endl;
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < images_per_subject; i++) {
        std::ifstream in(path + images.at(i), std::ios::in | std::ios::binary);
        std::ofstream out(reference_path + images.at(i), std::ios::out | std::ios::binary);
        out << in.rdbuf();
    }

    for (size_t i = images_per_subject; i < images.size(); i++) {
        std::ifstream in(path + images.at(i), std::ios::in | std::ios::binary);
        std::ofstream out(test_path + images.at(i), std::ios::out | std::ios::binary);
        out << in.rdbuf();
    }
}

int main(int argc, char *argv[]) {
    imageProcessing ip;

    for (int i = 1; i < 10; i++) {
        ip.quantize("../orl_faces/s0" + std::to_string(i) + "/", 128);
        ip.reduce_resolution("../orl_faces/s0" + std::to_string(i) + "/", 56, 46);
        ip.split_dataset("../orl_faces/s0" + std::to_string(i) + "/", 3);
    }

    for (int i = 10; i <= 40; i++) {
        ip.quantize("../orl_faces/s" + std::to_string(i) + "/", 128);
        ip.reduce_resolution("../orl_faces/s" + std::to_string(i) + "/", 56, 46);
        ip.split_dataset("../orl_faces/s" + std::to_string(i) + "/", 3);
    }
}