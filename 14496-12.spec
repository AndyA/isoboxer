
aligned(8) class Box (unsigned int(32) boxtype, optional unsigned int(8)[16] extended_type) {
  unsigned int(32) size;
  unsigned int(32) type = boxtype;
  if (size==1) {
    unsigned int(64) largesize;
  }
  else if (size==0) {
    // box extends to end of file
  }
  if (boxtype==‘uuid’) {
  unsigned int(8)[16] usertype = extended_type; }
}

aligned(8) class FullBox(unsigned int(32) boxtype, unsigned int(8) v, bit(24) f) extends Box(boxtype) {
  unsigned int(8) version = v;
  bit(24) flags = f;
}

aligned(8) class FileTypeBox

aligned(8) class MediaDataBox extends Box(‘mdat’) {
  bit(8) data[];
}

aligned(8) class FreeSpaceBox extends Box(free_type) {
  unsigned int(8) data[];
}

aligned(8) class ProgressiveDownloadInfoBox extends FullBox(‘pdin’, version = 0, 0) {
  for(i=0;;i++){
    //toendofbox unsigned int(32) rate;
    unsigned int(32) initial_delay;
  }
}

aligned(8) class MovieBox extends Box(‘moov’){
}

aligned(8) class MovieHeaderBox extends FullBox(‘mvhd’, version, 0) {
  if (version==1) {
    unsigned int(64)  creation_time;
    unsigned int(64)  modification_time;
    unsigned int(32)  timescale;
    unsigned int(64)  duration;
  }
  else {
    // version==0
    unsigned int(32)  creation_time;
    unsigned int(32)  modification_time;
    unsigned int(32)  timescale;
    unsigned int(32)  duration;
  }
  template int(32) rate = 0x00010000; // typically 1.0
  template int(16) volume = 0x0100; // typically, full volume const bit(16) reserved = 0;
  const unsigned int(32)[2] reserved = 0;
  template int(32)[9] matrix =
  {
  0x00010000,0,0,0,0x00010000,0,0,0,0x40000000 }
  ;
  // Unity matrix
  bit(32)[6]  pre_defined = 0;
  unsigned int(32)  next_track_ID;
}

aligned(8) class TrackBox extends Box(‘trak’) {
}

aligned(8) class TrackHeaderBox

aligned(8) class TrackReferenceBox extends Box(‘tref’) {
}

aligned(8) class TrackReferenceTypeBox (unsigned int(32) reference_type) extends Box(reference_type) {
  unsigned int(32) track_IDs[];
}

aligned(8) class MediaBox extends Box(‘mdia’) {
}

aligned(8) class MediaHeaderBox extends FullBox(‘mdhd’, version, 0) {
  if (version==1) {
    unsigned int(64)  creation_time;
    unsigned int(64)  modification_time;
    unsigned int(32)  timescale;
    unsigned int(64)  duration;
  }
  else {
    // version==0
    unsigned int(32)  creation_time;
    unsigned int(32)  modification_time;
    unsigned int(32)  timescale;
    unsigned int(32)  duration;
  }
  bit(1) pad=0;
  unsigned int(5)[3] language; // ISO-639-2/T language code unsigned int(16) pre_defined = 0;
}

aligned(8) class HandlerBox extends FullBox(‘hdlr’, version = 0, 0) {
  unsigned int(32) pre_defined = 0;
  unsigned int(32) handler_type;
  const unsigned int(32)[3] reserved = 0;
  string   name;
}

aligned(8) class MediaInformationBox extends Box(‘minf’) {
}

aligned(8) class VideoMediaHeaderBox

aligned(8) class SoundMediaHeaderBox

aligned(8) class HintMediaHeaderBox

aligned(8) class NullMediaHeaderBox

aligned(8) class SampleTableBox extends Box(‘stbl’) {
}

aligned(8) abstract class SampleEntry (unsigned int(32) format) extends Box(format){
  const unsigned int(8)[6] reserved = 0;
  unsigned int(16) data_reference_index;
}

class HintSampleEntry() extends SampleEntry (protocol) {
  unsigned int(8) data [];
}

class BitRateBox extends Box(‘btrt’){
  unsigned int(32) bufferSizeDB;
  unsigned int(32) maxBitrate;
  unsigned int(32) avgBitrate;
}

class MetaDataSampleEntry(codingname) extends SampleEntry (codingname) {
}

class XMLMetaDataSampleEntry() extends MetaDataSampleEntry (’metx‘) {
  string content_encoding; // optional
  string namespace;
  string schema_location; // optional
  BitRateBox (); // optional
}

class TextMetaDataSampleEntry() extends MetaDataSampleEntry (‘mett’) {
  string content_encoding; // optional
  string mime_format;
  BitRateBox (); // optional
}

class PixelAspectRatioBox extends Box(‘pasp’){
  unsigned int(32) hSpacing;
  unsigned int(32) vSpacing;
}

class CleanApertureBox extends Box(‘clap’){
  unsigned int(32) cleanApertureWidthN; unsigned int(32) cleanApertureWidthD;
  unsigned int(32) cleanApertureHeightN;
  unsigned int(32) cleanApertureHeightD;
  unsigned int(32) horizOffN;
  unsigned int(32) horizOffD;
  unsigned int(32) vertOffN;
  unsigned int(32) vertOffD;
}

class VisualSampleEntry(codingname) extends SampleEntry (codingname){
  unsigned int(16) pre_defined = 0;
  const unsigned int(16) reserved = 0;
  unsigned int(32)[3] pre_defined = 0;
  unsigned int(16) width;
  unsigned int(16) height;
  template unsigned int(32) horizresolution = 0x00480000; // 72 dpi template unsigned int(32) vertresolution = 0x00480000; // 72 dpi const unsigned int(32) reserved = 0;
  template unsigned int(16) frame_count = 1;
  string[32] compressorname;
  template unsigned int(16) depth = 0x0018;
  int(16) pre_defined = -1;
  CleanApertureBox clap; // optional
  PixelAspectRatioBox pasp; // optional
}

class AudioSampleEntry(codingname) extends SampleEntry (codingname){
  const unsigned int(32)[2] reserved = 0;
  template unsigned int(16) channelcount = 2;
  template unsigned int(16) samplesize = 16;
  unsigned int(16) pre_defined = 0;
  const unsigned int(16) reserved = 0 ;
  template unsigned int(32) samplerate = {
  default samplerate of media}
  <<16;
}

aligned(8) class SampleDescriptionBox (unsigned int(32) handler_type) extends FullBox('stsd', 0, 0){
  int i ;
  unsigned int(32) entry_count;
  for (i = 1 ; i <= entry_count ; i++){
    switch (handler_type){
      case ‘soun’: // for audio tracks
      AudioSampleEntry();
      break;
      case ‘vide’: // for video tracks
      VisualSampleEntry();
      break;
      case ‘hint’: // Hint track
      HintSampleEntry();
      break;
      case ‘meta’: // Metadata track
      MetadataSampleEntry();
    break;      }
  }
}

aligned(8) class DegradationPriorityBox extends FullBox(‘stdp’, version = 0, 0) {
  int i;
  for (i=0; i < sample_count; i++) {
    unsigned int(16)  priority;
  }
}

aligned(8) class SampleScaleBox extends FullBox(‘stsl’, version = 0, 0) {
  bit(7) reserved = 0;
  bit(1) constraint_flag;
  unsigned int(8) scale_method;
  int(16) display_center_x;
  int(16) display_center_y;
}

aligned(8) class TimeToSampleBox

aligned(8) class CompositionOffsetBox extends FullBox(‘ctts’, version = 0, 0) {
  unsigned int(32) entry_count;
  int i;
  for (i=0; i < entry_count; i++) {
    unsigned int(32)  sample_count;
    unsigned int(32)  sample_offset;
  }
}

aligned(8) class SyncSampleBox

aligned(8) class ShadowSyncSampleBox

aligned(8) class SampleDependencyTypeBox extends FullBox(‘sdtp’, version = 0, 0) {
  for (i=0; i < sample_count; i++){
    unsigned int(2) reserved = 0;
    unsigned int(2) sample_depends_on;
    unsigned int(2) sample_is_depended_on;
    unsigned int(2) sample_has_redundancy;
  }
}

aligned(8) class EditBox extends Box(‘edts’) {
}

aligned(8) class EditListBox extends FullBox(‘elst’, version, 0) {
  unsigned int(32) entry_count;
  for (i=1; i <= entry_count; i++) {
    if (version==1) {
      unsigned int(64) segment_duration;
      int(64) media_time;
    }
    else {
      // version==0
      unsigned int(32) segment_duration;
      int(32)  media_time;
    }
    int(16) media_rate_integer;
    int(16) media_rate_fraction = 0;
  }
}

aligned(8) class DataInformationBox extends Box(‘dinf’) {
}

aligned(8) class DataEntryUrlBox (bit(24) flags) extends FullBox(‘url ’, version = 0, flags) {
  string location;
}

aligned(8) class DataEntryUrnBox (bit(24) flags) extends FullBox(‘urn ’, version = 0, flags) {
  string name;
  string location;
}

aligned(8) class DataReferenceBox

aligned(8) class SampleSizeBox extends FullBox(‘stsz’, version = 0, 0) {
  unsigned int(32) sample_size;
  unsigned int(32) sample_count;
  if (sample_size==0) {
    for (i=1; i <= sample_count; i++) {
      unsigned int(32)  entry_size;
    }
  }
}

aligned(8) class CompactSampleSizeBox extends FullBox(‘stz2’, version = 0, 0) {
  unsigned int(24) reserved = 0;
  unisgned int(8) field_size;
  unsigned int(32) sample_count;
  for (i=1; i <= sample_count; i++) {
    unsigned int(field_size)   entry_size;
  }
}

aligned(8) class SampleToChunkBox

aligned(8) class ChunkOffsetBox

aligned(8) class ChunkLargeOffsetBox

aligned(8) class PaddingBitsBox extends FullBox(‘padb’, version = 0, 0) {
  unsigned int(32) sample_count;
  int i;
  for (i=0; i < ((sample_count + 1)/2); i++) {
    bit(1)   reserved = 0;
    bit(3)   pad1;
    bit(1)   reserved = 0;
    bit(3)   pad2;
  }
}

aligned(8) class SubSampleInformationBox extends FullBox(‘subs’, version, 0) {
  unsigned int(32) entry_count;
  int i,j;
  for (i=0; i < entry_count; i++) {
    unsigned int(32) sample_delta;
    unsigned int(16) subsample_count;
    if (subsample_count > 0) {
      for (j=0; j < subsample_count; j++) {
        if(version == 1)
        {
          unsigned int(32) subsample_size;
        }
        else {
          unsigned int(16) subsample_size;
        }
        unsigned int(8) subsample_priority;
        unsigned int(8) discardable;
        unsigned int(32) reserved = 0;
      }
    }
  }
}

aligned(8) class MovieExtendsBox extends Box(‘mvex’){
}

aligned(8) class MovieExtendsHeaderBox extends FullBox(‘mehd’, version, 0) {
  if (version==1) {
    unsigned int(64)  fragment_duration;
  }
  else {
    // version==0
    unsigned int(32)  fragment_duration;
  }
}

aligned(8) class TrackExtendsBox extends FullBox(‘trex’, 0, 0){
  unsigned int(32) track_ID;
  unsigned int(32) default_sample_description_index;
  unsigned int(32) default_sample_duration;
  unsigned int(32)  default_sample_size;
  unsigned int(32)  default_sample_flags
}

aligned(8) class MovieFragmentBox extends Box(‘moof’){
}

aligned(8) class MovieFragmentHeaderBox extends FullBox(‘mfhd’, 0, 0){
  unsigned int(32)  sequence_number;
}

aligned(8) class TrackFragmentBox extends Box(‘traf’){
}

aligned(8) class TrackFragmentHeaderBox extends FullBox(‘tfhd’, 0, tf_flags){
  unsigned int(32) track_ID;
  // all the following are optional fields unsigned int(64) base_data_offset; unsigned int(32) sample_description_index; unsigned int(32) default_sample_duration; unsigned int(32) default_sample_size; unsigned int(32) default_sample_flags
}

aligned(8) class TrackRunBox

aligned(8) class MovieFragmentRandomAccessBox extends Box(‘mfra’)

aligned(8) class TrackFragmentRandomAccessBox extends FullBox(‘tfra’, version, 0) {
  unsigned int(32)  track_ID;
  const unsigned int(26)  reserved = 0;
  unsigned int(2)
  unsigned int(2)
  unsigned int(2)
  unsigned int(32)  number_of_entry;
  for(i=1; i <= number_of_entry; i++){
    length_size_of_traf_num;
    length_size_of_trun_num;
    length_size_of_sample_num;
    if(version==1){
      unsigned int(64)  time;
      unsigned int(64)  moof_offset;
    }
    else{
      unsigned int(32)  time;
      unsigned int(32)  moof_offset;
    }
    unsignedint((length_size_of_traf_num+1)*8) traf_number; unsignedint((length_size_of_trun_num+1)*8) trun_number; unsigned int((length_size_of_sample_num+1) * 8)sample_number;
  }
}

aligned(8) class MovieFragmentRandomAccessOffsetBox extends FullBox(‘mfro’, version, 0) {
  unsigned int(32)  size;
}

aligned(8) class SampleToGroupBox

abstract class SampleGroupDescriptionEntry (unsigned int(32) grouping_type) {
}

abstract class VisualSampleGroupEntry (unsigned int(32) grouping_type) extends SampleGroupDescriptionEntry (grouping_type)

abstract class AudioSampleGroupEntry (unsigned int(32) grouping_type) extends SampleGroupDescriptionEntry (grouping_type)

abstract class HintSampleGroupEntry (unsigned int(32) grouping_type) extends SampleGroupDescriptionEntry (grouping_type)

aligned(8) class SampleGroupDescriptionBox (unsigned int(32) handler_type) extends FullBox('sgpd', version, 0){
  unsigned int(32) grouping_type;
  if (version==1) {
  unsigned int(32) default_length; }
  unsigned int(32) entry_count;
  int i;
  for (i = 1 ; i <= entry_count ; i++){
    if (version==1) {
      if (default_length==0) {
        unsigned int(32) description_length;
      }
    }
    switch (handler_type){
      case ‘vide’: // for video tracks VisualSampleGroupEntry (grouping_type); break;
      case ‘soun’: // for audio tracks AudioSampleGroupEntry(grouping_type); break;
      case ‘hint’: // for hint tracks HintSampleGroupEntry(grouping_type); break;
    }
  }
}

aligned(8) class UserDataBox extends Box(‘udta’) {
}

aligned(8) class CopyrightBox

aligned(8) class TrackSelectionBox

aligned(8) class MetaBox (handler_type) extends FullBox(‘meta’, version = 0, 0) {
  HandlerBox(handler_type) theHandler;
  PrimaryItemBox
  DataInformationBox
  ItemLocationBox
  ItemProtectionBox
  ItemInfoBox
  IPMPControlBox
  Box   other_boxes[];
  8.11.1.3 Semantics
  primary_resource;
  file_locations;
  item_locations;
  protections;
  item_infos;
  IPMP_control;
  // optional
  // optional
  // optional
  // optional
  // optional
  // optional
  // optional
}

aligned(8) class XMLBox

aligned(8) class BinaryXMLBox

aligned(8) class ItemLocationBox extends FullBox(‘iloc’, version = 0, 0) {
  unsigned int(4)
  unsigned int(4)
  unsigned int(4)
  unsigned int(4)
  unsigned int(16)  item_count;
  for (i=0; i<item_count; i++) {
    offset_size;
    length_size;
    base_offset_size;
    reserved;
    unsigned int(16) item_ID;
    unsigned int(16) data_reference_index; unsigned int(base_offset_size*8) base_offset; unsigned int(16) extent_count;
    for (j=0; j<extent_count; j++) {
      unsigned int(offset_size*8) extent_offset;
    unsigned int(length_size*8) extent_length; }
  }
}

aligned(8) class PrimaryItemBox

aligned(8) class ItemProtectionBox

aligned(8) class ItemInfoExtension(unsigned int(32) extension_type) {
}

aligned(8) class FDItemInfoExtension() extends ItemInfoExtension (’fdel’) {
  string            content_location;
  string            content_MD5;
  unsigned int(64)  content_length;
  unsigned int(64)  transfer_length;
  unsigned int(8)   entry_count;
  for (i=1; i <= entry_count; i++)
  unsigned int(32)  group_id;
}

aligned(8) class ItemInfoEntry

aligned(8) class ItemInfoBox

aligned(8) class AdditionalMetadataContainerBox extends Box('meco') {
}

aligned(8) class MetaboxRelationBox

aligned(8) class ProtectionSchemeInfoBox(fmt) extends Box('sinf') {
  OriginalFormatBox(fmt) original_format;
  IPMPInfoBox
  SchemeTypeBox
  SchemeInformationBox
  8.12.2 Original Format Box 8.12.2.1 Definition
  IPMP_descriptors; // optional
  scheme_type_box; // optional info; // optional
}

aligned(8) class OriginalFormatBox(codingname) extends Box ('frma') {
  unsigned int(32) data_format = codingname;
}

aligned (8) class IPMPInfoBox extends FullBox(‘imif’, 0, 0){
  IPMP_Descriptor ipmp_desc[];
}

aligned(8) class IPMPControlBox extends FullBox('ipmc', 0, flags) {
  IPMP_ToolListDescriptor toollist;
  int(8) no_of_IPMPDescriptors;
  IPMP_Descriptor ipmp_desc[no_of_IPMPDescriptors];
}

aligned(8) class SchemeTypeBox extends FullBox('schm', 0, flags) {
  unsigned int(32) scheme_type; // 4CC identifying the scheme unsigned int(32) scheme_version; // scheme version
  if (flags & 0x000001) {
  unsigned int(8) scheme_uri[]; // browser uri }
}

aligned(8) class SchemeInformationBox extends Box('schi') {
  Box scheme_specific_data[];
}

aligned(8) class PartitionEntry extends Box('paen') {
  FilePartitionBox blocks_and_symbols; FECReservoirBox FEC_symbol_locations; //optional
}

aligned(8) class FDItemInformationBox

aligned(8) class FilePartitionBox

aligned(8) class FECReservoirBox

aligned(8) class FDSessionGroupBox extends Box('segr') {
  unsigned int(16) num_session_groups;
  for(i=0; i < num_session_groups; i++) {
    unsigned int(8)   entry_count;
    for (j=0; j < entry_count; j++) {
      unsigned int(32)  group_ID;
    }
    unsigned int(16) num_channels_in_session_group; for(k=0; k < num_channels_in_session_group; k++) {
      unsigned int(32) hint_track_id;
    }
  }
}

aligned(8) class GroupIdToNameBox

class RtpHintSampleEntry() extends SampleEntry (‘rtp ‘) {
  uint(16) hinttrackversion = 1;
  uint(16) highestcompatibleversion = 1;
  uint(32) maxpacketsize;
  box         additionaldata[];
}

class timescaleentry() extends Box(‘tims’) {
  uint(32) timescale;
}

class timeoffset() extends Box(‘tsro’) {
  int(32)     offset;
}

class sequenceoffset extends Box(‘snro’) {
  int(32) offset;
}

class SrtpHintSampleEntry() extends SampleEntry (‘srtp‘) {
  uint(16) hinttrackversion = 1;
  uint(16) highestcompatibleversion = 1;
  uint(32) maxpacketsize;
  box         additionaldata[];
}

aligned(8) class SRTPProcessBox extends FullBox(‘srpp’, version, 0) {
  unsigned int(32)
  unsigned int(32)
  unsigned int(32)
  unsigned int(32)
  SchemeTypeBox
  SchemeInformationBox    info;
  encryption_algorithm_rtp;
  encryption_algorithm_rtcp;
  integrity_algorithm_rtp;
  integrity_algorithm_rtcp;
  scheme_type_box;
}

aligned(8) class RTPsample {
  unsigned int(16)  packetcount;
  unsigned int(16)  reserved;
  RTPpacket   packets[packetcount];
  byte     extradata[];
}

aligned(8) class RTPpacket {
  int(32) relative_time;
  // the next fields form initialization for the RTP
  // header (16 bits), and the bit positions correspond bit(2) reserved;
  bit(1) P_bit;
  bit(1) X_bit;
  bit(4) reserved;
  bit(1) M_bit;
  bit(7) payload_type;
  unsigned int(16)  RTPsequenceseed;
  unsigned int(13)  reserved = 0;
  unsigned int(1)
  unsigned int(1)
  unsigned int(1)
  unsigned int(16)  entrycount;
  if (extra_flag) {
    uint(32) extra_information_length;
    box   extra_data_tlv[];
  }
  dataentry   constructors[entrycount];
}

class rtpoffsetTLV() extends Box(‘rtpo’) {
  int(32) offset;
}

aligned(8) class RTPconstructor(type) {
  unsigned int(8) constructor_type = type;
}

aligned(8) class RTPnoopconstructor

aligned(8) class RTPimmediateconstructor

aligned(8) class RTPsampleconstructor extends RTPconstructor(2)

aligned(8) class RTPsampledescriptionconstructor extends RTPconstructor(3)

aligned(8) class rtpmoviehintinformation extends box(‘rtp ‘) {
  uint(32) descriptionformat = ‘sdp ‘;
  char sdptext[];
}

aligned(8) class trackhintinformation extends box(‘hnti’) {
}

aligned(8) class rtptracksdphintinformation extends box(‘sdp ‘) {
  char sdptext[];
}

aligned(8) class hintstatisticsbox extends box(‘hinf’) {
}

aligned(8) class hintBytesSent extends box(‘trpy’) {
uint(64) bytessent; }
// total bytes sent, including 12-byte RTP headers

aligned(8) class hintPacketsSent extends box(‘nump’) {
uint(64) packetssent; }
// total packets sent

aligned(8) class hintBytesSent extends box(‘tpyl’) {
uint(64) bytessent; }
// total bytes sent, not including RTP headers

aligned(8) class hintBytesSent extends box(‘totl’) {
uint(32) bytessent; }
// total bytes sent, including 12-byte RTP headers

aligned(8) class hintPacketsSent extends box(‘npck’) {
uint(32) packetssent; }
// total packets sent

aligned(8) class hintBytesSent extends box(‘tpay’) {
uint(32) bytessent; }
// total bytes sent, not including RTP headers

aligned(8) class hintmaxrate extends box(‘maxr’) {
  // maximum data rate uint(32) period; // in milliseconds
uint(32) bytes; }
// max bytes sent in any period ‘period’ long

aligned(8) class hintmediaBytesSent extends box(‘dmed’) {
uint(64) bytessent; }
// total bytes sent from media tracks

aligned(8) class hintimmediateBytesSent extends box(‘dimm’) {
uint(64) bytessent; }
// total bytes sent immediate mode

aligned(8) class hintrepeatedBytesSent extends box(‘drep’) {
uint(64) bytessent; }
// total bytes in repeated packets

class hintminrelativetime extends box(‘tmin’) {
time; }
// smallest relative transmission time, milliseconds

class hintmaxrelativetime extends box(‘tmax’) {
time; }
// largest relative transmission time, milliseconds

class hintlargestpacket extends box(‘pmax’) {
  aligned(8)
uint(32) bytes; }
// largest packet sent, including RTP header

aligned(8) class hintlongestpacket extends box(‘dmax’) {
uint(32) time; }
// longest packet duration, milliseconds

aligned(8) class hintpayloadID extends box(‘payt’) {
  uint(32) payloadID; // payload ID used in RTP packets
}

class FDHintSampleEntry() extends SampleEntry ('fdp ') {
  unsigned int(16) hinttrackversion = 1;
  unsigned int(16) highestcompatibleversion = 1; unsigned int(16) partition_entry_ID;
  unsigned int(16)  FEC_overhead;
  Box               additionaldata[];   //optional
}

aligned(8) class FDsample extends Box(‘fdsa’) {
  FDPacketBox packetbox[]
  ExtraDataBox extradata; //optional
}

aligned(8) class FDpacketBox extends Box(‘fdpa’) {
  LCTheaderTemplate LCT_header_info;
}

aligned(8) class LCTheaderTemplate {
}

aligned(8) class LCTheaderextension {
  unsigned int(8) header_extension_type;
  if (header_extension_type > 127) {
    unsigned int(8) content[3];
  }
  else {
    unsigned int(8) length;
    if (length > 0) {
      unsigned int(8) content[(length*4) - 2];
    }
  }
}

aligned(8) class FDconstructor(type) {
  unsigned int(8)   constructor_type = type;
}

aligned(8) class FDnoopconstructor extends FDconstructor(0) {
  unsigned int(8)   pad[15];
}

aligned(8) class FDimmediateconstructor extends FDconstructor(1) {
}

aligned(8) class FDsampleconstructor extends FDconstructor(2) {
  signed int(8)     trackrefindex;
  unsigned int(16)  length;
  unsigned int(32)  samplenumber;
  unsigned int(32)  sampleoffset;
  unsigned int(16)  bytesperblock = 1;
  unsigned int(16)  samplesperblock = 1;
}

aligned(8) class FDitemconstructor extends FDconstructor(3) {
  unsigned int(16) item_ID;
  unsigned int(16) extent_index;
  unsigned int(64) data_offset; //offset in byte within extent
  unsigned int(24) data_length; //non-zero length in byte within extent or
  //if (data_length==0) rest of extent
}

aligned(8) class FDxmlboxconstructor extends FDconstructor(4)

aligned(8) class ExtraDataBox extends Box(‘extr’) {
  bit(8) extradata[];
}

class VisualRollRecoveryEntry() extends VisualSampleGroupEntry (’roll’) {
  signed int(16) roll_distance;
}

class AudioRollRecoveryEntry() extends AudioSampleGroupEntry (’roll’) {
  signed int(16) roll_distance;
}

class RateShareEntry() extends SampleGroupDescriptionEntry('rash') {
  unsigned int(16) operation_point_count;
  if (operation_point_count == 1) {
    unsigned int(16)     target_rate_share;
  }
  else {
    for (i=0; i < operation_point_count; i++) {
      unsigned int(32)  available_bitrate;
      unsigned int(16)  target_rate_share;
    }
  }
  unsigned int(32)  maximum_bitrate;
  unsigned int(32)  minimum_bitrate;
  unsigned int(8)   discard_priority;
}
