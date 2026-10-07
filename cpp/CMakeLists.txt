cmake_minimum_required(VERSION 3.10)
project(bilan_thermique_cpp)

set(CMAKE_CXX_STANDARD 17)

include_directories(include)

set(SOURCES
    src/radiation.cpp
    src/glace.cpp
    src/chaleur_sensible.cpp
    src/chaleur_latente.cpp
    src/interfaces.cpp
    src/bilan.cpp
    src/csv_row.cpp
    main.cpp
)

add_executable(bilan_thermique ${SOURCES})
