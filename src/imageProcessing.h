//
// Created by Pedro Ferreira,
//            Rafael Direito,
//            Rafael Teixeira.
//

#include <string>
#include <iostream>
#include <opencv2/highgui/highgui.hpp>


class imageProcessing {
public:
    void quantize(const std::string& path, int q);

    void reduce_resolution(const std::string& path, int width, int height);

    void split_dataset();
};
