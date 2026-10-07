#include "csv_row.hpp"
#include <sstream>

CsvRow parse_csv_line(const std::string& line) {
    CsvRow row{};
    std::stringstream ss(line);
    std::string token;

    auto next_double = [&]() {
        std::getline(ss, token, ',');
        return std::stod(token);
    };

    row.Ta           = next_double();
    row.va           = next_double();
    row.HR           = next_double();
    row.Fi           = next_double();
    row.hi           = next_double();
    row.ha           = next_double();
    row.Tw           = next_double();
    row.AFDD         = next_double();
    row.ATDD         = next_double();
    row.NetRad       = next_double();

    std::getline(ss, token, ',');
    row.use_hi_mesure = std::stoi(token);

    return row;
}
