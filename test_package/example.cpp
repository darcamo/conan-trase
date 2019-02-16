#include <iostream>
#include <fstream>
#include "trase.hpp"

using namespace trase;

int main() {
    auto fig = figure();
    auto ax = fig->axis();
    const int n = 100;
    const int nframes = 10;
    std::vector<float> x(n);
    std::vector<float> y(n);

    // define x points
    for (int i = 0; i < n; ++i) {
        x[i] = static_cast<float>(i) / n;
    }

    // define y = sin(x) with given amplitude and frequency
    auto get_ysinx = [&](const float amplitude, const float freq) {
                         for (int i = 0; i < n; ++i) {
                             y[i] = amplitude * std::sin(6.28f * freq * x[i]);
                         }
                         return create_data().x(x).y(y);
                     };

    // create a static sin(x) function
    auto static_plot = ax->line(get_ysinx(1.f, 2.f));
    static_plot->set_label("static");

    // create a moving sin(x) function with varying amplitude
    auto moving_plot = ax->line(get_ysinx(1.f, 5.f));
    moving_plot->set_label("moving");

    for (int i = 1; i <= nframes; ++i) {
        const float nf = static_cast<float>(nframes);
        const float amplitude = 1.f - 0.5f * std::sin(6.28f * i / nf);
        moving_plot->add_frame(get_ysinx(amplitude, 5.f), 3.f * i / nf);
    }

    // set label axes
    ax->xlabel("x");
    ax->ylabel("y");
    ax->title("the svg test");
    ax->legend();

    // output to svg
    std::ofstream out;
    out.open("readme.svg");
    BackendSVG backend(out);
    fig->draw(backend);
    out.close();
}
