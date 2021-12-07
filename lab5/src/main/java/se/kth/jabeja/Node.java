package se.kth.jabeja;

import java.util.ArrayList;

public class Node {

	private int id;
	private int color;
	private int initColor;
	private ArrayList<Integer> neighbours;

	public Node(int id, int color) {
		this.id = id;
		this.color = color;
		this.initColor = color;
		this.neighbours = new ArrayList<Integer>();
	}

	public void setColor(int color) {
		this.color = color;
	}

	public void setNeighbours(ArrayList<Integer> neighbours) {
		for (int id : neighbours)
			this.neighbours.add(id);
	}
	
	public int getId() {
		return this.id;
	}
	public int getColor() {
		return this.color;
	}
	public int getDegree() {
		return this.neighbours.size();
	}
	public int getInitColor() {
		return this.initColor;
	}
	public ArrayList<Integer> getNeighbours() {
		return this.neighbours;
	}
	@Override
	public String toString() {
		return "id: " + id + ", color: " + color + ", neighbours: " + neighbours + "\n";
	}
}
