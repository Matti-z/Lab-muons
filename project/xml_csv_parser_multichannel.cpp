#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<vector>
#include<pugixml.hpp>
#include <cctype>
#include <chrono>
#include <iomanip>
#include "libraries/xml_parser.hpp"
#include "libraries/progress_bar.hpp"

// make
// #define LINE_LIMIT 100000
#define DELTA 400
#define DOUBLE_CHECK_LIMIT_INDEX 40
#define PULSE_WIDTH 12  



void usage(){
    std::cout << "Usage of the script:\n";
    std::cout << "./parser <xml path> <csv path> <cfg path>\n\n\n";
    std::cout << "the csv file will contain timestamps of signal peaks detected in each event\n";
    std::cout << "CSV Structure:\n";
    std::cout << "Single column containing timestamps (in seconds) measured from the end to the rising edge of the signal\n";
    std::cout << "Each row represents a timestamp detected in a single event\n";
    exit(0);
}



void check_multitrace(std::istringstream &iss,  bool &save, std::vector<std::vector<short>> &trace_vector, int channel)
{
    int x;
    int min = 0;
    int max = 0;

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
        trace_vector[channel].push_back(x);
    }
}

void triple_check(int last_trace_index, int traceStartingIndex ,double freq, std::vector<std::vector<short>> &trace_vector, std::vector<double> &timestamps)
{
    bool isTriggered = false;
    bool giunone_signal = false;
    bool tripla_in_discrimination = false; 
    bool hasPartenopeTriggered = false;
    
    std::vector<short> tripla = trace_vector[0];
    std::vector<short> partenope = trace_vector[1];
    std::vector<short> giunone = trace_vector[2];

    int baselineTripla = tripla[0];
    int baselineGiunone = giunone[0];
    int baselinePartenope = partenope[0]; 
    int startingLenght = timestamps.size();

    for (int traceIndex = traceStartingIndex; traceIndex > traceStartingIndex - PULSE_WIDTH ; traceIndex--){
        
        if (tripla[traceIndex] < baselineTripla - DELTA){
            tripla_in_discrimination = true;
            // traceStartingIndex = traceIndex;
            break;
        }
    }
    
    std::cout << tripla_in_discrimination << "\tDOPPIA TRIPLA\n";

    for (int traceIndex = traceStartingIndex; traceIndex >= 0; traceIndex--)
    {
        double timestamp = double(last_trace_index - traceIndex) / freq;
        if (tripla[traceIndex] < baselineTripla - DELTA && !isTriggered)
        {
            timestamps.push_back(timestamp);
            isTriggered = true;
            if (tripla_in_discrimination){
                
                if( timestamps.size() <= startingLenght) std::cout << "-------tripla in discrimination-------\n";
                timestamps.pop_back();
                continue;
            }
        }

        if (tripla[traceIndex] > baselineTripla - DELTA && isTriggered){
            isTriggered = false;
            tripla_in_discrimination = false;
            if( !giunone_signal) {
                if( timestamps.size() <= startingLenght) std::cout << "-------giunone-------\n";
                timestamps.pop_back();
                giunone_signal = false;
                continue;
            }
            giunone_signal = false;
        }
        
        if ( partenope[traceIndex] < baselinePartenope - DELTA && isTriggered && !hasPartenopeTriggered && !tripla_in_discrimination){
            if( timestamps.size() <= startingLenght) std::cout << "-------partenope-------\n";
            timestamps.pop_back();
            hasPartenopeTriggered = true;
            continue;
        }

        if ( partenope[traceIndex] > baselinePartenope - DELTA && hasPartenopeTriggered) hasPartenopeTriggered = false;
        
        if ( giunone[traceIndex]< baselineGiunone - DELTA && isTriggered) giunone_signal = true;
    }
}

void timestamp_calculator(int last_trace_index, double freq, std::vector<std::vector<short>> &trace_vector, std::vector<double> &timestamps , std::vector<bool> &dataset_discriminator)
{
    std::vector<short> partenope = trace_vector[1];
    std::vector<short> giunone = trace_vector[2];
    int baselineGiunone = giunone[0];
    int baselinePartenope = partenope[0];


    for( int g_index = last_trace_index ; g_index > last_trace_index - DOUBLE_CHECK_LIMIT_INDEX ; g_index--){
        if(giunone[g_index] < baselineGiunone - DELTA){
            std::cout << "giunone\n";
            triple_check(last_trace_index, g_index , freq, trace_vector, timestamps);
            while( dataset_discriminator.size() < timestamps.size()) dataset_discriminator.push_back(true);
            break;
        }
    }

    for( int p_index = last_trace_index ; p_index > last_trace_index - DOUBLE_CHECK_LIMIT_INDEX ; p_index--){
        if(partenope[p_index] < baselinePartenope - DELTA){
            std::cout << "partenope\n";
            triple_check(last_trace_index, p_index , freq, trace_vector, timestamps);
            while( dataset_discriminator.size() < timestamps.size()) dataset_discriminator.push_back(false);
            break;
        }
    }


}


void trace_to_timestamp(pugi::xml_node &event , std::vector<double>& timestamps , std::vector<bool> &discriminator, double freq , int size)
{
    std::string trace;
    int channel;
    int max_channel = -1;
    std::vector<std::vector<short>> trace_vector;
    
    int last_trace_index = size-1;

    bool save = false;

    // TRACE HAS 3 DATASET -> this will loop 3 times
    // This loop fills trace_vector with datas from A SINGULAR EVENT
    for (pugi::xml_node trace : event.children("trace")){

        channel = trace.attribute("channel").as_int();
        if ( channel > max_channel){
            max_channel = channel;
            trace_vector.push_back(std::vector<short>());
        }

        std::istringstream iss(trace.text().as_string());
        
        check_multitrace(iss, save, trace_vector, channel);

        if (trace_vector[channel].size() != size) { std::cout << "trace of unexpected size detected\n"; exit(-1); }
    }
    if (save) timestamp_calculator(last_trace_index, freq, trace_vector, timestamps , discriminator);
    std::cout<< timestamps.size() << "\t" << discriminator.size()<< "\n";
    
    if ( timestamps.size() != discriminator.size()){
        std::cout<< timestamps.size() << "\t" << discriminator.size()<< "\n";
        std::cout << "different size between timestamp array and isGiunoneDataset array\n";
        exit(-1);
    }

    trace_vector.clear();
}


void timestamp_to_csv(std::ofstream &out, std::vector<double> &timestamps , std::vector<bool> &divider)
{
    for( int i = 0 ; i < timestamps.size(); i++){
        out << timestamps[i] << " , " << divider[i] << "\n";
    }
}


int main(int argc, char const *argv[])
{
    //* INPUT FROM COMMAND LINE-------------------------------------------------------------------------------
    if (argc <= 1) usage();
    std::string xml_path = (argv[1] == "debug") ? "../big_data/triple_04_03_2026_05_12.xml" : argv[1];
    std::string csv_directory = (argc > 2) ? argv[2] : ".";
    std::string cfg_directory = (argc > 3) ? argv[3] : ".";
    //* -------------------------------------------------------------------------------

    //* VARIABLE DEFINITION -------------------------------------------------------------------------------
    if ( csv_directory.back() != '/' ) csv_directory.append("/");
    if ( cfg_directory.back() != '/' ) cfg_directory.append("/");
    std::string filename = xml_path.substr(xml_path.find_last_of("/\\") + 1);
    filename = filename.substr(0, filename.find_last_of("."));
    std::string csv_file = csv_directory + filename + ".csv";
    std::string cfg_file = cfg_directory + filename + "_cfg.csv";

    std::cout << filename << xml_path;
    //* ------------------------------------------------------------------------------- 

    

    //* OPEN FILES -------------------------------------------------------------------------------
    std::ifstream in(xml_path.c_str());
    std::ofstream out( csv_file.c_str());
    std::ofstream cfg( cfg_file.c_str());
    if (!in.is_open()){
        std::cout << "XML not Found\n";
        exit(-1);
    }
    if (!out.is_open()){
        std::cout << "CSV not Found\n";
        exit(-1);
    }
    if (!cfg.is_open()){
        std::cout << "CSV_settings not Found\n";
        exit(-1);
    }
    //* -------------------------------------------------------------------------------


    //* VARIABLE DEFINITION -------------------------------------------------------------------------------
    pugi::xml_document settings;
    pugi::xml_document digitizer;

    int size;
    double freq_hz;


    std::vector<double> timestamp;
    std::vector<std::vector<double>> multichannel_timestamp; 
    std::vector<bool> dataset_divider;
    
    pugi::xml_document history;
    pugi::xml_node events;
    //* -------------------------------------------------------------------------------

    //* SETTINGS PARSE -------------------------------------------------------------------------------
    setting_parser( "<digitizer>" , in , digitizer);
    setting_parser( "<settings>" , in , settings);
    
    pugi::xml_node window = settings.child("settings").child("window");
    size = window.attribute("size").as_int();

    
    pugi::xml_node freq = digitizer.child("digitizer").child("frequency");
    freq_hz = freq.attribute("hz").as_float();

    settings_to_csv( digitizer , settings , cfg);
    cfg.close();
    //* -------------------------------------------------------------------------------


    
    int max_ID = readLastEventId(xml_path , size);
    std::cout<<"Number of Events: \t"<< max_ID<<"\n";




    
    // Process events until end of file
    while( in.peek() != EOF ){

        event_parser(in , events , history);
        
        
        // Extract and store event data from XML
        for( pugi::xml_node event : events.children("event")){
            
            int id = event.attribute("id").as_int();
            // progressBar(float(id)/float(max_ID) , id);

            std::cout << id << "\t ID \n";
            trace_to_timestamp( event , timestamp , dataset_divider,  freq_hz , size);
        }
    }
    std::cout << std::endl;
    std::cout<<"-----------------------------------\t XML PARSED\t-----------------------------------\n";
    std::cout<<"events detected:\t" << timestamp.size() << "\t events triggered:\t"<< max_ID << "\n";
    timestamp_to_csv(out , timestamp , dataset_divider);

    
    return 0;
}

