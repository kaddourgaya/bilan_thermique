#pragma once
#include <string>

struct CsvRow {
    double Ta;
    double va;
    double HR;
    double Fi;
    double hi;
    double ha;
    double Tw;
    double AFDD;
    double ATDD;
    double NetRad;
    int    use_hi_mesure;
};

CsvRow parse_csv_line(const std::string& line);
