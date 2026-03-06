CXX = g++
CXXFLAGS = -Wall
LDFLAGS = -lpugixml


TARGET = csv_parser
SOURCES = xml_csv_parser.cpp progress_bar.cpp xml_parser.cpp
OBJECTS = $(SOURCES: .cpp=.o)

# result file needs all object files
$(TARGET): $(OBJECTS)
# 	compiler command with .o files
	$(CXX) $(OBJECTS) $(LDFLAGS) -o $(TARGET)

%.o:%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS) $(TARGET)

.PHONY: clean