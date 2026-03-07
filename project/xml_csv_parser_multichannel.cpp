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
#define DELTA 500
#define DOUBLE_CHECK_LIMIT_INDEX 50



void usage(){
    std::cout << "Usage of the script:\n";
    std::cout << "./parser <xml path> <csv path> <cfg path>\n\n\n";
    std::cout << "the csv file will contain timestamps of signal peaks detected in each event\n";
    std::cout << "CSV Structure:\n";
    std::cout << "Single column containing timestamps (in seconds) measured from the end to the rising edge of the signal\n";
    std::cout << "Each row represents a timestamp detected in a single event\n";
    exit(0);
}



int check_multitrace(std::istringstream &iss,  bool &save, std::vector<std::vector<short>> &trace_vector, int channel)
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
    return max;
}

bool triple_check(int last_trace_index, double freq, std::vector<std::vector<short>> &trace_vector, int max, std::vector<double> &values)
{
    bool trigger = false;
    bool giunone_signal = false;
    bool fake_triple = false;
    std::vector<short> tripla = trace_vector[0];
    std::vector<short> partenope = trace_vector[1];
    std::vector<short> giunone = trace_vector[2];
    for (int traceIndex = last_trace_index; traceIndex >= 0; traceIndex--)
    {
        double timestamp = double(last_trace_index - traceIndex) / freq;
        if (tripla[traceIndex] < max - DELTA && !trigger)
        {
            values.push_back(timestamp);
            trigger = true;
        }
        if (tripla[traceIndex] > max - DELTA && trigger){
            trigger = false;
            if( !giunone_signal) return true;
            giunone_signal = false;

        }
        
        if ( partenope[traceIndex] < max - DELTA && trigger ){
            values.pop_back();
            return true;
        }
        
        if ( giunone[traceIndex]< max - DELTA && trigger) giunone_signal = true;
        
    }
    return fake_triple;
}

void timestamp_calculator(int last_trace_index, double freq, std::vector<std::vector<short>> &trace_vector, int max, std::vector<double> &values , std::vector<bool> dataset_discriminator)
{
    std::vector<short> partenope = trace_vector[1];
    std::vector<short> giunone = trace_vector[2];
    bool fake_triple = false;

    for( int g_index = last_trace_index ; g_index < last_trace_index - DOUBLE_CHECK_LIMIT_INDEX ; g_index--){
        if(giunone[g_index] < max - DELTA){
            fake_triple = triple_check(last_trace_index, freq, trace_vector, max, values);
            if( !fake_triple) dataset_discriminator.push_back(true);
            break;
        }
    }

    for( int p_index = last_trace_index ; p_index < last_trace_index - DOUBLE_CHECK_LIMIT_INDEX ; p_index--){
        if(partenope[p_index] < max - DELTA){
            fake_triple = triple_check(last_trace_index, freq, trace_vector, max, values);
            if( !fake_triple) dataset_discriminator.push_back(false);
            break;
        }
    }


}


void trace_to_timestamp(pugi::xml_node &event , std::vector<double>& values , std::vector<bool> &discriminator, double freq , int size)
{
    std::string trace;
    int channel;
    int max;
    std::vector<std::vector<short>> trace_vector;
    
    int last_trace_index = size-1;

    // Parse trace values into vector
    bool save = false;
    for (pugi::xml_node trace : event.children("trace")){
        channel = event.child("trace").attribute("samples").as_int();
        std::istringstream iss(trace.text().as_string());

        max = check_multitrace(iss, save, trace_vector, channel);



        if (trace_vector[channel].size() != size) { std::cout << "trace of unexpected size detected\n"; exit(0); }
    
    }
    if (save) timestamp_calculator(last_trace_index, freq, trace_vector, max, values , discriminator);
    
    if ( values.size() != discriminator.size()){
        std::cout << "different size between discriminator array and values array";
        exit(0);
    }

    trace_vector.clear();
}


void timestamp_to_csv(std::ofstream &out, std::vector<double> &values , std::vector<bool> &divider)
{
    for( int i = 0 ; i < values.size(); i++){
        out << values[i] << " , " << divider[i] << "\n";
    }
}


int main(int argc, char const *argv[])
{
    //* INPUT FROM COMMAND LINE-------------------------------------------------------------------------------
    if (argc <= 1) usage();
    std::string xml_path = (argv[1] == "debug") ? "../big_data/16_1_2026_16_55.xml" : argv[1];
    std::cout<<xml_path<<"\n";
    std::string csv_directory = (argc > 2) ? argv[2] : ".";
    std::string cfg_directory = (argc > 3) ? argv[3] : ".";
    //* -------------------------------------------------------------------------------

    //* VARIABLE DEFINITION -------------------------------------------------------------------------------
    if ( csv_directory.back() != '/' ) csv_directory.append("/");
    if ( cfg_directory.back() != '/' ) cfg_directory.append("/");
    std::string filename = xml_path.substr(xml_path.find_last_of("/\\") + 1).substr(0, filename.find_last_of("."));
    std::string csv_file = csv_directory + filename + ".csv";
    std::string cfg_file = cfg_directory + filename + "_cfg.csv";
    //* ------------------------------------------------------------------------------- 

    

    //* OPEN FILES -------------------------------------------------------------------------------
    std::ifstream in(xml_path.c_str());
    std::ofstream out( csv_file.c_str());
    std::ofstream cfg( cfg_file.c_str());
    if (!in.is_open()){
        std::cout << "XML not Found\n";
        exit(0);
    }
    if (!out.is_open()){
        std::cout << "CSV not Found\n";
        exit(0);
    }
    if (!cfg.is_open()){
        std::cout << "CSV_settings not Found\n";
        exit(0);
    }
    //* -------------------------------------------------------------------------------


    //* VARIABLE DEFINITION -------------------------------------------------------------------------------
    pugi::xml_document settings;
    pugi::xml_document digitizer;

    int size;
    double freq_hz;
    int max_ID = readLastEventId(xml_path , size);

    std::vector<double> timestamp;
    std::vector<std::vector<double>> multichannel_timestamp; 
    std::vector<bool> dataset_divider;

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
    //* -------------------------------------------------------------------------------


    

    std::cout<<"Number of Events: \t"<< max_ID<<"\n";




    
    // Process events until end of file
    while( in.peek() != EOF ){

        event_parser(in , events);
        
        // Extract and store event data from XML
        for( pugi::xml_node event : events.children("event")){
            int id = event.attribute("id").as_int();
            progressBar(float(id)/float(max_ID) , id);

            trace_to_timestamp( event , timestamp , dataset_divider,  freq_hz , size);
        }
    }
    std::cout << std::endl;
    std::cout<<"-----------------------------------\t XML PARSED\t-----------------------------------\n";
    std::cout<<"events detected:\t" << timestamp.size() << "\t events triggered:\t"<< max_ID << "\n";
    timestamp_to_csv(out , timestamp , dataset_divider);

    
    return 0;
}

