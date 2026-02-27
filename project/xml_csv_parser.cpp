#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<vector>
#include<pugixml.hpp>
#include <cctype>
#include <chrono>
#include <iomanip>


// g++ -o csv_parser xml_csv_parser.cpp -I/opt/homebrew/include -L/opt/homebrew/lib -lpugixml
// g++ -o csv_parser xml_csv_parser.cpp -lpugixml
#define LINE_LIMIT 100000
#define DELTA 500


#define XML_ENDER "</digitizer>"

static auto start_time = std::chrono::high_resolution_clock::now();

void usage(){
    std::cout << "Usage of the script:\n";
    std::cout << "./parser <xml path> <csv path> <cfg path>\n\n\n";
    std::cout << "the csv file will contain timestamps of signal peaks detected in each event\n";
    std::cout << "CSV Structure:\n";
    std::cout << "Single column containing timestamps (in seconds) measured from the end to the rising edge of the signal\n";
    std::cout << "Each row represents a timestamp detected in a single event\n";
    exit(0);
}

void setting_parser( std::string starter, std::ifstream& in , std::string& content){
    
    std::string line;

    std::string ender = starter;
    ender.insert(1 , "/");
    starter.pop_back();
    while(std::getline(in, line) && line.find(starter) != 0){}
    content += line + "\n";
    while(std::getline(in , line) && line != ender) content += line + "\n";
    content += line + "\n";
}

void settings_to_csv(pugi::xml_document &digitizer, pugi::xml_document &settings , std::ofstream& cfg)
{
    double freq_hz;
    int resolution;
    float volt_low;
    float volt_high;
    float postTrg_float;
    int size;

    // DIGITIZER CLASS
    pugi::xml_node freq = digitizer.child("digitizer").child("frequency");
    freq_hz = freq.attribute("hz").as_float();
    pugi::xml_node volt_limit = digitizer.child("digitizer").child("voltagerange");
    volt_low = volt_limit.attribute("low").as_float();
    volt_high = volt_limit.attribute("hi").as_float();
    pugi::xml_node res = digitizer.child("digitizer").child("resolution");
    resolution = res.attribute("bits").as_int();



    // SETTINGS CLASS
    pugi::xml_node trg = settings.child("settings").child("posttrigger");
    std::string postTrg = trg.attribute("value").as_string();
    postTrg_float = std::stof(postTrg.substr(0, postTrg.length() - 1));
    pugi::xml_node window = settings.child("settings").child("window");
    size = window.attribute("size").as_int();

    std::string full_cfg = 
    "frequency[hz]," + std::to_string(freq_hz) + ",\n" +
    "resolution[bytes]," + std::to_string(resolution) + ",\n" +
    "volt_low[V]," + std::to_string(volt_low) + ",\n" +
    "volt_high[V]," + std::to_string(volt_high) + ",\n" +
    "postTrg[%]," + std::to_string(postTrg_float) + ",\n" +
    "size[bits]," + std::to_string(size) + ",\n" +
    "delta[bits]," + std::to_string(DELTA) + ",\n";

    cfg << full_cfg;

}

void event_parser( std::ifstream& in , std::string& content){
    
    int counter = 0;

    std::string line;
    std::string starter = "<event>";
    std::string ender = starter;
    ender.insert(1 , "/");
    starter.pop_back();
    while(std::getline(in, line) && line.find(starter) != 0);
    content += line + "\n";
    while(std::getline(in, line) && !(counter >= LINE_LIMIT && line == ender) ){
        content += line + "\n";
        counter++;
    }
    content += line + "\n";
}


void trace_to_timestamp(pugi::xml_node &event , std::vector<double>& values , double freq , int size)
{
    std::string trace;
    trace = event.child("trace").text().as_string();

    std::istringstream iss(trace);
    std::vector<short> trace_vector;
    
    int x;
    int last_trace_index = size-1;

    // Parse trace values into vector
    int min = 0;
    int max = 0;
    bool save = false;
    bool trigger = false;
    while (iss >> x)
    {
        if (!save)
        {
            if ((min == 0) && (max == 0))
            {
                min = x;
                max = x;
            }
            if (x < min)
                min = x;
            if (x > max)
                max = x;
            if (max - min > DELTA)
                save = true;
        }
        trace_vector.push_back(x);
    }
    if (trace_vector.size() != size){
        std::cout << "trace of unexpected size detected\n";
        exit(0);
    }
    if (save)
        for( int traceIndex = size-1 ; traceIndex >=0 ; traceIndex-- ){
            double timestamp = double(last_trace_index - traceIndex)/freq;
            if( trace_vector[traceIndex]< max - DELTA && !trigger){
                values.push_back(timestamp);
                trigger = true;
            }
            if ( trace_vector[traceIndex] > max - DELTA && trigger) trigger = false;
        }
    trace_vector.clear();
}

void timestamp_to_csv( std::ofstream& out, std::vector<double>& values){
    for( int i = 0 ; i < values.size(); i++){
        out << values[i] << ",\n";
    }
}



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

int main(int argc, char const *argv[])
{

    if (argc <= 1) usage();
    std::string xml_path = (argv[1] == "debug") ? argv[1] : "../big_data/16_1_2026_16_55.xml";
    std::cout<<xml_path<<"\n";
    std::string csv_directory = (argc > 2) ? argv[2] : ".";
    std::string cfg_directory = (argc > 3) ? argv[3] : ".";


    if ( csv_directory.back() != '/' ) csv_directory.append("/");
    if ( cfg_directory.back() != '/' ) cfg_directory.append("/");
    std::string filename = xml_path.substr(xml_path.find_last_of("/\\") + 1);
    filename = filename.substr(0, filename.find_last_of("."));


    std::string csv_file = csv_directory + filename + ".csv";
    std::string cfg_file = cfg_directory + filename + "_cfg.csv";

    

    // Open the XML input file
    std::ifstream in(xml_path.c_str());
    std::ofstream out( csv_file.c_str());
    std::ofstream cfg( cfg_file.c_str());
    std::string content;
    if (!in.is_open()){
        std::cout << "XML not Found\n";
        exit(0);
    }
    if (!out.is_open()){
        std::cout << "CSV not Found\n";
        exit(0);
    }

    


    // Parse digitizer settings from XML
    setting_parser( "<digitizer>" , in , content);
    pugi::xml_document digitizer;
    digitizer.load_string(content.c_str());
    content.clear();

    // Parse general settings from XML
    setting_parser( "<settings>" , in , content);
    pugi::xml_document settings;
    
    settings.load_string(content.c_str());
    content.clear();

    int size;
    pugi::xml_node window = settings.child("settings").child("window");
    size = window.attribute("size").as_int();

    double freq_hz;
    pugi::xml_node freq = digitizer.child("digitizer").child("frequency");
    freq_hz = freq.attribute("hz").as_float();

    settings_to_csv( digitizer , settings , cfg);


    int max_ID = readLastEventId(xml_path , size);

    std::cout<<"Number of Events: \t"<< max_ID<<"\n";
    
    std::cout<<"settings parsed\n";


    // definition vector for timestamps
    std::vector<double> values; 

    
    // Process events until end of file
    while( in.peek() != EOF ){

        content += "<events>\n",
        event_parser(in , content);
        content += "</events>\n";



        // Parse event data from XML string
        pugi::xml_document history;
        history.load_string(content.c_str());
        pugi::xml_node events = history.child("events");
        // clear string
        content.clear();
        
        
        
        // Extract and store event data from XML
        for( pugi::xml_node event : events.children("event")){
            int id = event.attribute("id").as_int();
            progressBar(float(id)/float(max_ID) , id);

            trace_to_timestamp( event , values , freq_hz , size);
        }
    }
    std::cout << std::endl;
    std::cout<<"-----------------------------------\t XML PARSED\t-----------------------------------\n";
    std::cout<<"events detected:\t" << values.size() << "\t events triggered:\t"<< max_ID << "\n";
    timestamp_to_csv(out , values);

    
    return 0;
}

