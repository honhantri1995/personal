# Run 'make' or 'make all' to build executable file
# Run 'make clean' to remove all object files and executable files
# Run 'make depend' to use makedepend to automatically generate dependencies (which are added to end of Makefile)

# Define the compiler to use ('gcc' if C, or 'g++' if C++)
CC = g++

# Define the removing rule (this also overrides the default RM flag of Make)
RM = rm -f

# Define compiler flags
#   For example, '-Wall' enables all warnings, '-g' adds debug info, '-std=c++17' uses C++17 standard
CFLAGS = -Wall -g -std=c++17
# Preprocessors:
CFLAGS +=

# Define directories containing libraries other than /usr/lib
#   The rule is appending '-L' before the directory name 
LFLAGS = -L/usr/local/lib

# Define names of libraries to link into executable:
#   The rule is appending '-l' before the lib name 
#   For example, to link in libraries mylib.so or mylib.a, use -lmylib (no extension)
LIBS = 

# Define the C++ source files
SRC_DIR_1 = .
SRC_FILES := $(shell find $(SRC_DIR_1) -name '*.c')

# Define directories containing header files other than /usr/include
#   The rule is appending '-I' before the directory name
INC_DIR_1 = .
INC_DIR_2 = ../common
HEADERS = -I$(INC_DIR_1) -I$(INC_DIR_2)

# Define the executable file's name
EXE = server

# Running 'make' will invoke the first target entry in the file 
# You can name this target entry anything, but "default" or "all" are the convention
all: $(EXE)
	echo "All source files have been compiled"

# Compiling and Linking: Create the executable file from source files
$(EXE):
	$(CC) $(CFLAGS) $(HEADERS) $(SRC_FILES) $(LFLAGS) $(LIBS) -o $(EXE)

# Running 'make clean' removes the executable file, all .o files and *~ backup files
clean:
	$(RM) *.o *~ $(EXE)
	$(RM) $(SRC_DIR_1)/*.o

# Running 'make depend' generates dependencies of Cpp source files automatically
#    Install makedepend on Ubuntu: sudo apt-get install xutils-dev
depend: $(SRC_FILES)
	makedepend $(HEADERS) $^

# DO NOT DELETE THIS LINE -- make depend needs it
