#!/bin/bash
for filename in *.xyz; do
  sed -i '1,2d' "$filename"
  sed -i '1i! sp Def2/JK RIJK m062x d3zero def2-svp verytightscf XYZfile Grid5 FinalGrid6 veryslowconv' "$filename"
  sed -i '2i%pal' "$filename"
  sed -i '3inprocs 5' "$filename"
  sed -i '4iend' "$filename"
  sed -i '5i!CPCM(octanol)' "$filename"
  sed -i '6i%cpcm' "$filename"
  sed -i '7ismd true' "$filename"
  sed -i '8iSMDsolvent "1-octanol"' "$filename"  
  sed -i '9iend' "$filename"
  sed -i '10i!nomoprint' "$filename"
  sed -i '11i!miniprint' "$filename"  
  sed -i '12i!nomayer' "$filename"  
  sed -i '13i!nomulliken' "$filename"  
  sed -i '14i!nopop' "$filename"  
  sed -i '15i* xyz 0 1' "$filename"
  cat orca_geomOpt_append.txt >> "$filename"
  cat "$filename" >> "$filename".inp
  echo "$filename"
done
