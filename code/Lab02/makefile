# Compiler
CC = g++

# Compiler flags
CFLAGS = -Wall -g -std=c++14

# Executable name
EXE = main

# Source files
SRC = ExtendiableHashing.cpp Main.cpp

# Object files
OBJ = $(SRC:.cpp=.o)

# Header files
HDR = ExtendiableHashing.h

# Compile the program
$(EXE): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(EXE)

# Compile the source files
%.o: %.cpp $(HDR)
	$(CC) $(CFLAGS) -c $<

# Clean the files
clean:
	rm -f $(OBJ) $(EXE)

