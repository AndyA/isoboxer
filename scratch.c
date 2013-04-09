/* scratch.c */

#include <stdio.h>

/* How do we make the box size available to the reader once we know it?
 * Has to be a special case because the box size is otherwise unremarkable.
 * Probably easiest just to allow some boxes to be overridden with hand written
 * handlers.
 *
 * How do we know not to read the data in pure data boxes?
 */

static void Box(jd_var *out, reader *r) {
  uint32_t size = r->get_32u(r);
  uint32_t type = r->get_32u(r);
  uint64_t box_size = size;
  if (size == 1) {
    box_size = r->get_64u(r);
    r->assign_64u(r, out, "largesize", box_size);
  }
  else if (size == 0) {
    // extends to end of file
  }
  if (type == FOURCC("uuid")) {
    r->read_array(r, out, "usertype", r->read_8u, 16);
  }
  r->assign_32u(r, out, "size", size);
  r->assign_32u(r, out, "type", type);

  /* manually set reader limit, hidden field */
  r->set_box_size(r, box_size);
  r->assign_64u(r, out, "_size", box_size);
}

static void FullBox(jd_var *out, reader *r) {
  Box(out, r);
  r->read_8u(r, out, "version");
  r->read_bits(r, out, "flags", 24);
}

static void FileTypeBox(jd_var *out, reader *r) {
  Box(out, r);
  r->check(r, out, "type", FOURCC("ftyp"));
  r->read_32u(r, out, "major_brand");
  r->read_32u(r, out, "minor_version");
  r->read_to_end(r, out, "compatible_brands", r->read_32u);
}

static void MediaDataBox(void) {
}

static void FreeSpaceBox(void) {
}

int main(void) {
  return 0;
}

/* vim:ts=2:sw=2:sts=2:et:ft=c
 */
