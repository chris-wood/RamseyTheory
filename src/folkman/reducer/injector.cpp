// File: injector.cpp
// Author: Christopher Wood

#include <iostream>
#include <deque>
#include <iterator>

#include <boost/graph/adjacency_list.hpp>

using namespace std;

int main()
{
    // Create a n adjacency list, add some vertices.
    boost::adjacency_list<> g(num tasks);
    boost::add_vertex(0, g);
    boost::add_vertex(1, g);
    boost::add_vertex(2, g);
    boost::add_vertex(3, g);
    boost::add_vertex(4, g);
    boost::add_vertex(5, g);
    boost::add_vertex(6, g);

    // Add edges between vertices.
    boost::add_edge(0, 3, g);
    boost::add_edge(1, 3, g);
    boost::add_edge(1, 4, g);
    boost::add_edge(2, 1, g);
    boost::add_edge(3, 5, g);
    boost::add_edge(4, 6, g);
    boost::add_edge(5, 6, g);

    return 0;
}