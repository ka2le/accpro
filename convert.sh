#!/bin/bash

for f in msh/*.msh
do
	dolfin-convert $f ${f:0:-3}xml
done