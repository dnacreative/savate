/* bitrates */
extern int MPEG_1_LAYER_1[16] = {
    -1, 32000, 64000, 96000, 128000, 160000, 192000, 224000, 256000, 288000,
    320000, 352000, 384000, 416000, 448000, -1
};

extern int MPEG_1_LAYER_2[16] = {
    -1, 32000, 48000, 56000, 64000, 80000, 96000, 112000, 128000, 160000,
    192000, 224000, 256000, 320000, 384000, -1
};

extern int MPEG_1_LAYER_3[16] = {
    -1, 32000, 40000, 48000, 56000, 64000, 80000, 96000, 112000, 128000,
    160000, 192000, 224000, 256000, 320000, -1
};

extern int MPEG_2_LAYER_1[16] = {
    -1, 32000, 48000, 56000, 64000, 80000, 96000, 112000, 128000, 144000,
    160000, 176000, 192000, 224000, 256000, -1
};

extern int MPEG_2_LAYER_2_3[16] = {
    -1, 8000, 16000, 24000, 32000, 40000, 48000, 56000, 64000, 80000, 96000,
    112000, 128000, 144000, 160000, -1
};
/* end bitrates */

/* sampling rate frequency */
extern int FREQUENCIES[3][4] = {
    {44100, 48000, 32000, -1},
    {22050, 24000, 16000, -1},
    {11025, 12000, 8000, -1}
};