aligned(8) class Box(unsigned int(32) boxtype, 
                     optional unsigned int(8)[16] extended_type) {
  unsigned int(32) size;
  unsigned int(32) type = boxtype;
  if (size==1) {
    unsigned int(64) largesize;
  } 
  else if (size==0) {
    // box extends to end of file
  }
  if (boxtype==‘uuid’) {
    unsigned int(8)[16] usertype = extended_type;
  }
}

aligned(8) class FullBox(unsigned int(32) boxtype, 
                         unsigned int(8) v, bit(24) f) extends Box(boxtype) {
  unsigned int(8) version = v;
  bit(24) flags = f;
}

aligned(8) class FileTypeBox extends Box(‘ftyp’) {
  unsigned int(32) major_brand;
  unsigned int(32) minor_version;
  unsigned int(32) compatible_brands[]; // to end of the box
}

aligned(8) class MediaDataBox extends Box('mdat') {
  bit(8) data[];
}

aligned(8) class FreeSpaceBox extends Box(free_type) {
  unsigned int(8) data[];
}
