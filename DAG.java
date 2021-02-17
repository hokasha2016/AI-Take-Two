import java.io;
import java.util;

public class DAG {
    Node root;

    public static class Node{
        List<Node> successors;
        int value;
    }
}