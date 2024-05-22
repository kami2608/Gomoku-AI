#include <pybind11/pybind11.h>

#include <AIWine.h>
#include <Board.h>
#include <Chess.h>
#include <ChessShape.h>
#include <HashTable.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)


namespace py = pybind11;

PYBIND11_MODULE(cmake_example, m) {
    m.doc() = "AIWine module";

    py::class_<HashTable>(m, "HashTable")
    .def(py::init<>());

    py::class_<Board>(m, "Board")
    .def(py::init<HashTable*>())
    .def("initBoard", &Board::initBoard, "Initialize the board")
    .def("move", &Board::move, "Make a move on the board")
    .def("undo", &Board::undo, "Undo the last move")
    .def("evaluate", &Board::evaluate, "Evaluate the board")
    .def("vcfSearch", py::overload_cast<int*>(&Board::vcfSearch), "VCF Search")
    .def("vctSearch", py::overload_cast<int*>(&Board::vctSearch), "VCT Search");

    py::class_<ChessShape>(m, "ChessShape")
    .def_static("initShape", &ChessShape::initShape, "Initialize shapes");

    py::class_<Chess>(m, "Chess")
    .def(py::init<>())
    .def("update1", &Chess::update1, "Update 1")
    .def("update4", &Chess::update4, "Update 4")
    .def("updateShape", &Chess::updateShape, "Update shape");

    py::class_<AIWine>(m, "AIWine")
    .def(py::init<>())
    .def("setSize", &AIWine::setSize, "Set the size of board")
    .def("restart", &AIWine::restart, "Restart the game")
    .def("turnUndo", &AIWine::turnUndo, "Undo the last move")
    .def("turnMove", &AIWine::turnMove, "Make a move")
    .def("turnBest", [](AIWine &ai) {
        int x, y;
        ai.turnBest(x, y);
        return std::make_pair(x, y);
    }, "Get the best move")
    .def("isValidPos", &AIWine::isValidPos, "Check valid position")
    .def("stopTime", &AIWine::stopTime, "Get stop time")
    .def("getTime", &AIWine::getTime, "Get current time")
    .def_readonly_static("MaxSize", &AIWine::MaxSize)
    .def_readonly_static("MaxDepth", &AIWine::MaxDepth)
    .def_readonly_static("MinDepth", &AIWine::MinDepth)
    .def_readonly_static("MaxCand", &AIWine::MaxCand);;

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
