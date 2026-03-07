#include <chrono>
#include<iostream>
#include <fstream>
#include <iomanip>
#include <vector>

static auto start_time = std::chrono::high_resolution_clock::now();

void progressBar(float progress , int id) {
    
    auto current_time = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(current_time - start_time).count();
    
    
    float rate = float(id)/float(elapsed);
    
    int width = 50;
    int pos = static_cast<int>(width * progress);

    std::cout << "[";
    for (int i = 0; i < width; ++i) {
        if (i < pos) std::cout << "=";
        else if (i == pos) std::cout << ">";
        else std::cout << " ";
    }
    std::cout << "] \t" << int(progress * 100) << "%\t" << id << "\t" << std::fixed << std::setprecision(0) << rate << " events/s \r";
    std::cout.flush();
}


int readLastEventId(const std::string& filename , int size) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) return -1;

    file.seekg(0, std::ios::end);
    std::streamoff pos = file.tellg();

    size_t CHUNK = size;
    std::string buffer;

    while (pos > 0) {
        size_t readSize = std::min(CHUNK, (size_t)pos);
        pos -= readSize;
        file.seekg(pos);

        std::vector<char> chunk(readSize);
        file.read(chunk.data(), readSize);

        buffer.insert(0, chunk.data(), readSize);

        // search from the back
        auto evt = buffer.rfind("<event");
        if (evt != std::string::npos) {
            auto idPos = buffer.find("id=", evt);
            if (idPos == std::string::npos)
                return -1;

            idPos += 3; // skip "id="

            // skip optional quotes
            if (buffer[idPos] == '"' || buffer[idPos] == '\'')
                ++idPos;

            int id = 0;
            while (idPos < buffer.size() && std::isdigit(buffer[idPos])) {
                id = id * 10 + (buffer[idPos] - '0');
                ++idPos;
            }
            return id;
        }
    }
    return -1;
}


