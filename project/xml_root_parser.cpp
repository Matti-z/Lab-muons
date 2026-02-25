#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<pugixml.hpp>
#include <cctype>
#include<TFile.h>
#include<TTree.h>
#include <iomanip>


// g++ -o parser xml_root_parser.cpp $(root-config --cflags --libs) -I/opt/homebrew/include -L/opt/homebrew/lib -lpugixml
// g++ -o parser xml_root_parser.cpp $(root-config --cflags --libs) -lpugixml
#define LINE_LIMIT 100000
#define DELTA 500
#define AUTO_FLUSH 500000
#define AUTO_SAVE 100000

#define XML_ENDER "</digitizer>"

static auto start_time = std::chrono::high_resolution_clock::now();

void usage(){
    std::cout << "Usage of the script:\n";
    std::cout << "./parser <xml path> <root path>\n\n\n";
    std::cout << "the root path will be the directory in which it will be saved different root files, each with a structure:\n";
    std::cout << "Tree: settings \t containing all useful characteristics of the dataset\n";
    std::cout << "|Branch: freq_hz\t containing frequency of data taken\n";
    std::cout << "|Branch: resolution\t containing bits of precisions in Y axis\n";
    std::cout << "|Branch: volt_low \t containing lowest voltage\n";
    std::cout << "|Branch: volt_high \t containing highest voltage\n";
    std::cout << "|Branch: post_trigger \t containing post-trigger percentage\n";
    std::cout << "|Branch: data_len \t containing data length\n";
    std::cout << "Tree:event \t tree containing all the data";
    std::cout << "| Branch: event [id] \t containing dataset of specific event with [id] = id\n";
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

void add_settings_to_root(pugi::xml_document &digitizer, pugi::xml_document &settings)
{
    double freq_hz;
    int resolution;
    float volt_low;
    float volt_high;
    float postTrg_float;
    int size;

    // ROOT INSERTION
    TTree tree("settings", "settings-of-the-dataset");
    tree.Branch("freq_hz", &freq_hz, "frequency_Hz/D");
    tree.Branch("resolution" , &resolution , "resolution_y_axis/I");
    tree.Branch("volt_low", &volt_low, "lowest-voltage_V/F");
    tree.Branch("volt_high", &volt_high, "highest-voltage_V/F");
    tree.Branch("post_trigger", &postTrg_float, "post-trigger_percentage/F");
    tree.Branch("data_len", &size, "data-lenght/I");

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

    
    tree.Fill();
    tree.Write();

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


void trace_to_root(pugi::xml_node &event , std::vector<short>& values , TTree *tree)
{
    std::string trace;
    trace = event.child("trace").text().as_string();

    std::istringstream iss(trace);

    int x;

    // Parse trace values into vector
    int min = 0;
    int max = 0;
    bool save = false;
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
        values.push_back(x);
    }
    if (save)
        tree->Fill();
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
    std::string xml_path = (argc > 1) ? argv[1] : "Lab-muons/digitizer/prova_xml.xml";
    std::cout<<xml_path<<"\n";
    std::string root_directory = (argc > 2) ? argv[2] : ".";


    if ( root_directory.back() != '/' ) root_directory.append("/");
    std::string filename = xml_path.substr(xml_path.find_last_of("/\\") + 1);
    filename = filename.substr(0, filename.find_last_of("."));

    

    // Open the XML input file
    std::ifstream in(xml_path.c_str());
    std::string content;
    if (!in.is_open()){
        std::cout << "File not Found\n";
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

    int max_ID = readLastEventId(xml_path , size);

    std::cout<<"Number of Events: \t"<< max_ID<<"\n";
    
    std::cout<<"settings parsed\n";

    
    


    // string definition for root file
    std::string root_file = root_directory + "file.root";
    std::string tree_name = "events";
    std::string branch_name = "events";

    // definition vector for branch
    std::vector<short> values; 
    
    
    // initializing TTree and TBranch
    // TFile rootFile( root_file.c_str() , "RECREATE", "" , ROOT::CompressionSettings(ROOT::kZSTD, 1));
    TFile rootFile( root_file.c_str() , "RECREATE");
    TTree *tree = new TTree(tree_name.c_str() , tree_name.c_str());
    TBranch *branch = tree->Branch(branch_name.c_str(), &values);

    tree->SetAutoSave(AUTO_SAVE);
    tree ->SetAutoFlush((int)AUTO_FLUSH);

    // Write settings to ROOT tree
    add_settings_to_root(digitizer, settings);
    
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
            // std::cout<<trace<<"\n";
            trace_to_root(event , values , tree);
            values.clear();

        }

        
    }

    std::cout.flush();
    // Write tree to file and close
    tree->Write("", TObject::kOverwrite);
    rootFile.Close();
    std::cout<<"-----------------------------------\t XML PARSED\t-----------------------------------\n";
    return 0;
}

