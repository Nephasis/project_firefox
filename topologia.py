#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from math import *
import time

class Topologia:
    def __init__(self, in_file):
        # Tworzy variables, ktore na początku sa puste
        self.atoms = []
        self.distances = []
        self.pairs = []
        self.angles = []
        self.dihedrals = []
        # Wczytuje atomy do listy atoms przez funkcje split and clean wykonana na pliku in.
        with open(in_file) as f:
            for line in f:
                self.atoms.append(self.__split_and_clean(line[:-1]))

    #Tworzy tablice(macierz) o wymiarach ilosci atomow, jakie bierzemy pod uwage, a nastepnie wpisuje obliczony dystans miedzy atomami
    #Do odpowiednich pozycji macierzy
    def calculate_distances(self):
        self.distances = [[0 for x in xrange(len(self.atoms)+1)] for x in xrange(len(self.atoms)+1)]
        for atom in self.atoms:
            for another_atom in self.atoms:
                self.distances[atom[0]][another_atom[0]] = self.__distance(atom, another_atom)

    #Wypisuje z macierzy (iterujac tak, aby zaden element sie nie powtarzal) dystanse spelniajace wymagane kryteria
    def write_down_distances(self, name):
        i = 0
        with open(name, 'w') as top:
            top.write('[bonds] \n')
            for i in xrange(len(self.distances)):
                j = i + 1
                while j < len(self.distances):
                    if self.distances[i][j] > 0:
                        top.write('  %d  %d\n' % (i, j))
                        self.pair = [i, j]
                        self.pairs.append(self.pair)
                    j += 1

    def write_angles_dihedrals(self, name):
        self.__clear_angles()
        with open(name, 'a') as top:
            top.write('\n[pairs]\n')
            for i in xrange(len(self.dihedrals)):
                top.write('  %s        %s\n' % (self.dihedrals[i][0], self.dihedrals[i][3]))
            top.write('\n[angles]\n')
            for i in xrange(len(self.angles)):
                top.write('  %s  %s  %s\n' % (self.angles[i][0], self.angles[i][1], self.angles[i][2]))
            top.write('\n[dihedrals]\n')
            for i in xrange(len(self.dihedrals)):
                top.write('  %s %s %s %s\n' % (self.dihedrals[i][0], self.dihedrals[i][1], self.dihedrals[i][2], self.dihedrals[i][3]))

    #PRIVATE CLASSES

    #Liczy dystans miedzy punktami
    def __distance(self, p0, p1):
        self.dist = (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2 + (p0[3] - p1[3])**2
        if self.dist < 0.025:
            return self.dist
        else:
            return -1

    #Dzieli linijki, usuwa puste elementy i zamienia stringi na floaty.
    def __split_and_clean(self, l):
        self.splited = l.split(' ')
        self.digits = []
        for item in self.splited:
            if item != '' and item.isdigitu() == True:
                self.digits.append(int(item))
            elif item != '':
                try:
                    self.digits.append(float(item))
                except ValueError:
                    pass
        return self.digits

    #Zwraca liste atomow polaczonych z atomem a1
    def __look_for_pair(self, a1):
        self.paired = []
        for i in xrange(len(self.pairs)):
            if self.pairs[i][0] == a1:
                self.paired.append(self.pairs[i][1])
            if self.pairs[i][1] == a1:
                self.paired.append(self.pairs[i][0])
        return self.paired

    #Tworzy liste atomow tworzacych katy
    def __look_for_angle(self, x):
        self.atoms2 = self.__look_for_pair(x)
        for atom in xrange(len(self.atoms2)):
            a2 = self.atoms2[atom]
            self.atoms3 = self.__look_for_pair(a2)
            if self.atoms3 != []:
                for at in xrange(len(self.atoms3)):
                    a3 = self.atoms3[at]
                    if a3 != x:
                        self.angle = [x, a2, a3]
                        self.angles.append(self.angle)
                        self.atoms4 = self.__look_for_pair(a3)
                        if self.atoms4 != []:
                            for atm in xrange(len(self.atoms4)):
                                a4 = self.atoms4[atm]
                                if a4 != x and a4 != a2 and a4 != a3:
                                    self.dihedral = [x, a2, a3, a4]
                                    self.dihedrals.append(self.dihedral)

    #Usuwa powtarzajace sie katy
    def __clear_angles(self):
        for atom in xrange(len(self.atoms)):
            self.__look_for_angle(atom)
        for i in self.angles:
            for j in self.angles:
                if i[0] == j[2] and i[2] == j[0]:
                    self.angles.remove(j)
        for i in self.dihedrals:
            for j in self.dihedrals:
                if i[0] == j[2] and i[2] == j[0] or i[0] == j[3] and i[3] == j[0]:
                    self.dihedrals.remove(j)

if __name__ == '__main__':
    script, input_file, output_file = argv

    topologia = Topologia(input_file)
    topologia.calculate_distances()
    time.sleep(180)
    topologia.write_down_distances(output_file)
    topologia.write_angles_dihedrals(output_file)
