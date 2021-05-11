from algorithm.TheQ import Q

#filelocation = "C:/Users/Kricx/Documents/GIT/theq/data/devdata"

def TheQFuntion(filelocation):
    """
        Currently its a mock
    :param filelocation: dirictory of input files
    :return: ListofFiles,WCCFXList,PlotDataList,QUnloaded,DataToSave
    """
    print("TheQFunction got path: {}".format(filelocation))
    (ListofFiles,WCCFXList,PlotDataList,QUnloaded,DataToSave) = Q(filelocation)
    return (ListofFiles,WCCFXList,PlotDataList,QUnloaded,DataToSave)


"""
    return (
        ['bruker_1601.s2p', 'fujikura_1601.s2p', 'fujikura_201.s2p'],
        [(8170796692.508812, 54727.15518984045), (7895290829.462796, 83700.3787612967), (7895290832.099763, 83699.84776072523)],
        [(([0.0077455, 0.00782579, 0.00790766, 0.00799115, 0.00807629,
                 0.00816316, 0.00825179, 0.00834225, 0.00843458, 0.00852884,
                 0.0086251, 0.00872343, 0.00882387, 0.00892651, 0.00903142,
                 0.00913867, 0.00924834, 0.00936051, 0.00947526, 0.00959269,
                 0.00971289, 0.00983596, 0.00996199, 0.0100911, 0.01022339,
                 0.01035899, 0.01049802, 0.01064061, 0.01078688, 0.010937,
                 0.0110911, 0.01124934, 0.0114119, 0.01157893, 0.01175064,
                 0.01192721, 0.01210884, 0.01229576, 0.01248819, 0.01268638,
                 0.01289057, 0.01310104, 0.01331808, 0.01354199, 0.01377309,
                 0.01401172, 0.01425825, 0.01451306, 0.01477656, 0.0150492,
                 0.01533143, 0.01562376, 0.01592672, 0.01624087, 0.01656682,
                 0.01690523, 0.01725679, 0.01762225, 0.01800241, 0.01839814,
                 0.01881036, 0.01924007, 0.01968835, 0.02015636, 0.02064536,
                 0.0211567, 0.02169186, 0.02225241, 0.02284009, 0.02345675,
                 0.02410443, 0.02478533, 0.02550184, 0.02625656, 0.02705232,
                 0.0278922, 0.02877953, 0.02971794, 0.03071137, 0.0317641,
                 0.03288071, 0.03406617, 0.03532579, 0.03666522, 0.0380904,
                 0.03960752, 0.04122289, 0.04294275, 0.04477304, 0.04671896,
                 0.04878441, 0.05097117, 0.05327774, 0.05569776, 0.0582178,
                 0.06081457, 0.06345116, 0.06607253, 0.06860025, 0.07092699,
                 0.07291197, 0.07437919, 0.07512145, 0.07491366, 0.07353841,
                 0.07082367, 0.06668717, 0.06117494, 0.05447813, 0.04691647,
                 0.03888915, 0.03080821, 0.02303641, 0.01584657, 0.00940822,
                 0.00379639, -0.00098737, -0.00499078, -0.00828949, -0.01097089,
                 -0.01312334, -0.01482974, -0.0161644, -0.01719193, -0.01796729,
                 -0.01853661, -0.01893821, -0.01920372, -0.01935911, -0.01942565,
                 -0.01942073, -0.01935857, -0.01925075, -0.01910675, -0.0189343,
                 -0.0187397, -0.01852811, -0.01830375, -0.01807004, -0.01782981,
                 -0.01758532, -0.01733844, -0.01709069, -0.01684328, -0.0165972,
                 -0.01635325, -0.01611205, -0.0158741, -0.01563979, -0.0154094,
                 -0.01518317, -0.01496126, -0.01474376, -0.01453075, -0.01432226,
                 -0.01411829, -0.01391883, -0.01372384, -0.01353326, -0.01334703,
                 -0.01316508, -0.01298733, -0.0128137, -0.01264408, -0.0124784,
                 -0.01231654, -0.01215843, -0.01200397, -0.01185304, -0.01170558,
                 -0.01156147, -0.01142063, -0.01128296, -0.01114838, -0.0110168,
                 -0.01088814, -0.01076231, -0.01063922, -0.01051881, -0.010401,
                 -0.01028571, -0.01017286, -0.0100624, -0.00995425, -0.00984834,
                 -0.00974462, -0.00964302, -0.00954348, -0.00944595, -0.00935036,
                 -0.00925667, -0.00916482, -0.00907476, -0.00898645, -0.00889983,
                 -0.00881486, -0.00873149, -0.00864969, -0.00856941, -0.00849061,
                 -0.00841326, -0.0083373, -0.00826272, -0.00818947, -0.00811752,
                 -0.00804684, -0.00797739, -0.00790914, -0.00784207, -0.00777614,
                 -0.00771132, -0.0076476, -0.00758494, -0.00752332, -0.0074627,
                 -0.00740308, -0.00734442]), ([0.005396, 0.00543366, 0.00547186, 0.00551062, 0.00554995,
                                                    0.00558986, 0.00563037, 0.00567148, 0.0057132, 0.00575556,
                                                    0.00579856, 0.00584221, 0.00588653, 0.00593153, 0.00597723,
                                                    0.00602363, 0.00607075, 0.00611861, 0.00616723, 0.0062166,
                                                    0.00626676, 0.00631771, 0.00636946, 0.00642205, 0.00647547,
                                                    0.00652974, 0.00658488, 0.00664091, 0.00669784, 0.00675567,
                                                    0.00681444, 0.00687414, 0.0069348, 0.00699643, 0.00705903,
                                                    0.00712263, 0.00718723, 0.00725284, 0.00731946, 0.00738711,
                                                    0.00745579, 0.0075255, 0.00759625, 0.00766802, 0.00774081,
                                                    0.00781461, 0.0078894, 0.00796518, 0.0080419, 0.00811954,
                                                    0.00819805, 0.0082774, 0.00835752, 0.00843833, 0.00851976,
                                                    0.0086017, 0.00868405, 0.00876665, 0.00884936, 0.00893199,
                                                    0.00901432, 0.0090961, 0.00917703, 0.00925678, 0.00933496,
                                                    0.00941111, 0.0094847, 0.00955513, 0.00962167, 0.00968351,
                                                    0.0097397, 0.00978911, 0.00983045, 0.00986222, 0.00988265,
                                                    0.00988968, 0.00988091, 0.00985351, 0.00980417, 0.00972898,
                                                    0.00962336, 0.00948188, 0.00929812, 0.00906449, 0.00877196,
                                                    0.00840983, 0.00796536, 0.00742337, 0.00676581, 0.00597119,
                                                    0.00501398, 0.00386395, 0.00248543, 0.00083672, -0.00113048,
                                                    -0.00347115, -0.00624641, -0.00952175, -0.01336347, -0.01783229,
                                                    -0.02297335, -0.02880192, -0.03528507, -0.04232148, -0.04972434,
                                                    -0.0572153, -0.06443812, -0.07099719, -0.07651694, -0.0807067,
                                                    -0.08340973, -0.08462001, -0.08446393, -0.08315808, -0.08096023,
                                                    -0.07812767, -0.07488964, -0.07143414, -0.06790531, -0.06440732,
                                                    -0.06101114, -0.05776181, -0.05468515, -0.05179323, -0.04908875,
                                                    -0.04656816, -0.04422406, -0.0420468, -0.04002559, -0.03814927,
                                                    -0.03640681, -0.03478755, -0.03328145, -0.03187913, -0.03057193,
                                                    -0.02935189, -0.02821173, -0.02714482, -0.02614513, -0.02520717,
                                                    -0.02432598, -0.02349703, -0.02271623, -0.02197985, -0.02128451,
                                                    -0.02062715, -0.02000494, -0.01941535, -0.01885605, -0.01832491,
                                                    -0.01781999, -0.0173395, -0.01688183, -0.01644546, -0.01602903,
                                                    -0.01563127, -0.01525101, -0.01488719, -0.0145388, -0.01420493,
                                                    -0.01388473, -0.01357741, -0.01328225, -0.01299857, -0.01272573,
                                                    -0.01246314, -0.01221028, -0.01196661, -0.01173168, -0.01150502,
                                                    -0.01128624, -0.01107493, -0.01087073, -0.01067331, -0.01048234,
                                                    -0.01029752, -0.01011856, -0.0099452, -0.00977719, -0.00961429,
                                                    -0.00945627, -0.00930294, -0.00915408, -0.0090095, -0.00886904,
                                                    -0.00873252, -0.00859978, -0.00847068, -0.00834506, -0.00822279,
                                                    -0.00810374, -0.0079878, -0.00787483, -0.00776473, -0.0076574,
                                                    -0.00755274, -0.00745064, -0.00735101, -0.00725378, -0.00715885,
                                                    -0.00706615, -0.0069756, -0.00688713, -0.00680066, -0.00671613,
                                                    -0.00663349, -0.00655266, -0.00647359, -0.00639622, -0.0063205,
                                                    -0.00624638, -0.00617381, -0.00610274, -0.00603313, -0.00596493,
                                                    -0.00589809, -0.00583259]),
          ([0.00776247, 0.00784255, 0.0079242, 0.00800746, 0.00809239,
                 0.00817904, 0.00826745, 0.00835768, 0.00844978, 0.00854382,
                 0.00863986, 0.00873795, 0.00883817, 0.00894058, 0.00904526,
                 0.00915227, 0.00926171, 0.00937364, 0.00948816, 0.00960535,
                 0.00972531, 0.00984813, 0.00997392, 0.01010278, 0.01023483,
                 0.01037018, 0.01050896, 0.01065129, 0.01079731, 0.01094717,
                 0.01110101, 0.01125899, 0.01142128, 0.01158805, 0.01175948,
                 0.01193578, 0.01211714, 0.01230378, 0.01249593, 0.01269383,
                 0.01289773, 0.01310791, 0.01332466, 0.01354827, 0.01377906,
                 0.01401739, 0.0142636, 0.0145181, 0.01478128, 0.01505359,
                 0.01533549, 0.01562749, 0.0159301, 0.01624391, 0.01656951,
                 0.01690756, 0.01725875, 0.01762384, 0.01800362, 0.01839896,
                 0.01881078, 0.01924009, 0.01968796, 0.02015555, 0.02064412,
                 0.02115502, 0.02168972, 0.02224982, 0.02283702, 0.0234532,
                 0.02410038, 0.02478077, 0.02549676, 0.02625095, 0.02704616,
                 0.02788547, 0.02877223, 0.02971005, 0.03070289, 0.031755,
                 0.03287099, 0.03405583, 0.03531481, 0.0366536, 0.03807814,
                 0.03959463, 0.04120939, 0.04292866, 0.0447584, 0.04670382,
                 0.04876885, 0.0509553, 0.05326168, 0.05568167, 0.0582019,
                 0.06079911, 0.06343644, 0.06605891, 0.06858811, 0.07091673,
                 0.07290396, 0.07437368, 0.07511851, 0.0749131, 0.07353965,
                 0.07082578, 0.06668891, 0.06117499, 0.05447531, 0.04691003,
                 0.0388789, 0.03079451, 0.02302001, 0.01582845, 0.00938936,
                 0.00377765, -0.00100532, -0.00500748, -0.00830466, -0.0109844,
                 -0.01313515, -0.01483992, -0.01617305, -0.01719917, -0.01797326,
                 -0.01854145, -0.01894206, -0.01920671, -0.01936135, -0.01942726,
                 -0.01942181, -0.01935919, -0.019251, -0.0191067, -0.018934,
                 -0.01873921, -0.01852748, -0.01830301, -0.01806924, -0.01782897,
                 -0.01758448, -0.01733763, -0.01708992, -0.01684257, -0.01659658,
                 -0.01635272, -0.01611163, -0.01587381, -0.01563963, -0.01540939,
                 -0.01518331, -0.01496155, -0.01474422, -0.01453138, -0.01432307,
                 -0.01411928, -0.01392, -0.0137252, -0.01353481, -0.01334878,
                 -0.01316703, -0.01298948, -0.01281604, -0.01264663, -0.01248115,
                 -0.0123195, -0.0121616, -0.01200734, -0.01185662, -0.01170937,
                 -0.01156547, -0.01142484, -0.01128738, -0.01115301, -0.01102165,
                 -0.01089319, -0.01076757, -0.0106447, -0.0105245, -0.0104069,
                 -0.01029182, -0.01017919, -0.01006894, -0.009961, -0.0098553,
                 -0.00975179, -0.0096504, -0.00955107, -0.00945375, -0.00935838,
                 -0.00926489, -0.00917326, -0.00908341, -0.0089953, -0.00890889,
                 -0.00882413, -0.00874098, -0.00865939, -0.00857931, -0.00850072,
                 -0.00842358, -0.00834783, -0.00827346, -0.00820041, -0.00812867,
                 -0.00805819, -0.00798895, -0.00792091, -0.00785404, -0.00778832,
                 -0.00772371, -0.00766019, -0.00759774, -0.00753632, -0.00747591,
                 -0.00741649, -0.00735804]), ([0.00540322, 0.00544073, 0.00547879, 0.00551741, 0.00555659,
                                                    0.00559636, 0.00563673, 0.00567769, 0.00571928, 0.00576149,
                                                    0.00580435, 0.00584786, 0.00589204, 0.00593689, 0.00598245,
                                                    0.00602871, 0.00607569, 0.00612341, 0.00617188, 0.00622111,
                                                    0.00627113, 0.00632193, 0.00637355, 0.00642599, 0.00647927,
                                                    0.0065334, 0.0065884, 0.00664429, 0.00670107, 0.00675877,
                                                    0.00681739, 0.00687696, 0.00693748, 0.00699897, 0.00706143,
                                                    0.00712489, 0.00718935, 0.00725482, 0.00732131, 0.00738882,
                                                    0.00745737, 0.00752694, 0.00759755, 0.00766919, 0.00774185,
                                                    0.00781552, 0.00789018, 0.00796583, 0.00804242, 0.00811994,
                                                    0.00819833, 0.00827755, 0.00835755, 0.00843825, 0.00851956,
                                                    0.0086014, 0.00868363, 0.00876613, 0.00884874, 0.00893127,
                                                    0.00901351, 0.0090952, 0.00917605, 0.00925573, 0.00933384,
                                                    0.00940993, 0.00948348, 0.00955386, 0.00962038, 0.0096822,
                                                    0.00973838, 0.0097878, 0.00982917, 0.00986098, 0.00988148,
                                                    0.0098886, 0.00987994, 0.00985269, 0.00980352, 0.00972855,
                                                    0.00962318, 0.00948199, 0.00929858, 0.00906535, 0.00877329,
                                                    0.0084117, 0.00796783, 0.00742654, 0.00676977, 0.00597603,
                                                    0.00501982, 0.00387088, 0.00249358, 0.00084617, -0.00111964,
                                                    -0.00345886, -0.00623266, -0.00950661, -0.0133471, -0.01781498,
                                                    -0.02295554, -0.02878424, -0.0352683, -0.04230649, -0.04971201,
                                                    -0.05720629, -0.0644327, -0.07099513, -0.07651746, -0.08070859,
                                                    -0.0834116, -0.08462059, -0.08446225, -0.08315358, -0.08095275,
                                                    -0.07811734, -0.07487684, -0.07141931, -0.06788893, -0.06438986,
                                                    -0.06099299, -0.05774332, -0.05466659, -0.05177483, -0.04907068,
                                                    -0.04655055, -0.044207, -0.04203036, -0.04000981, -0.03813418,
                                                    -0.03639241, -0.03477386, -0.03326846, -0.03186684, -0.03056032,
                                                    -0.02934095, -0.02820144, -0.02713516, -0.02613608, -0.02519872,
                                                    -0.02431809, -0.0234897, -0.02270944, -0.02197358, -0.02127874,
                                                    -0.02062186, -0.02000013, -0.01941099, -0.01885213, -0.01832142,
                                                    -0.01781691, -0.01733682, -0.01687953, -0.01644354, -0.01602748,
                                                    -0.01563007, -0.01525017, -0.01488668, -0.01453862, -0.01420507,
                                                    -0.01388518, -0.01357817, -0.01328331, -0.01299991, -0.01272736,
                                                    -0.01246506, -0.01221246, -0.01196906, -0.01173439, -0.01150799,
                                                    -0.01128946, -0.0110784, -0.01087445, -0.01067726, -0.01048653,
                                                    -0.01030193, -0.0101232, -0.00995007, -0.00978228, -0.00961959,
                                                    -0.00946179, -0.00930867, -0.00916001, -0.00901565, -0.00887539,
                                                    -0.00873907, -0.00860653, -0.00847761, -0.00835219, -0.00823011,
                                                    -0.00811125, -0.00799549, -0.0078827, -0.00777279, -0.00766564,
                                                    -0.00756115, -0.00745923, -0.00735978, -0.00726272, -0.00716796,
                                                    -0.00707543, -0.00698505, -0.00689674, -0.00681044, -0.00672608,
                                                    -0.0066436, -0.00656293, -0.00648402, -0.00640682, -0.00633126,
                                                    -0.00625729, -0.00618488, -0.00611396, -0.0060445, -0.00597645,
                                                    -0.00590977, -0.00584442])),
         (([0.00439733, 0.00439951, 0.00440169, ..., -0.00825126,
                 -0.00823645, -0.00822169]), ([-0.02208898, -0.02212173, -0.02215457, ..., 0.02561281,
                                                    0.0255834, 0.02555407]),
          ([0.00447874, 0.00448079, 0.00448281, ..., -0.00832465,
                 -0.00830987, -0.00829537]), ([-0.02211418, -0.02214721, -0.0221798, ..., 0.02558023,
                                                    0.02555056, 0.02552144])),
         (([4.41215597e-03, 4.42924673e-03, 4.44608560e-03, 4.46264433e-03,
                 4.47889272e-03, 4.49479803e-03, 4.51032521e-03, 4.52543643e-03,
                 4.54009114e-03, 4.55424538e-03, 4.56785199e-03, 4.58086017e-03,
                 4.59321497e-03, 4.60485730e-03, 4.61572335e-03, 4.62574416e-03,
                 4.63484530e-03, 4.64294645e-03, 4.64996052e-03, 4.65579357e-03,
                 4.66034368e-03, 4.66350060e-03, 4.66514488e-03, 4.66514682e-03,
                 4.66336573e-03, 4.65964897e-03, 4.65383045e-03, 4.64572964e-03,
                 4.63514993e-03, 4.62187718e-03, 4.60567791e-03, 4.58629735e-03,
                 4.56345706e-03, 4.53685278e-03, 4.50615125e-03, 4.47098751e-03,
                 4.43096133e-03, 4.38563304e-03, 4.33451945e-03, 4.27708873e-03,
                 4.21275476e-03, 4.14087096e-03, 4.06072286e-03, 3.97152001e-03,
                 3.87238669e-03, 3.76235139e-03, 3.64033419e-03, 3.50513362e-03,
                 3.35540991e-03, 3.18966714e-03, 3.00623195e-03, 2.80322892e-03,
                 2.57855264e-03, 2.32983448e-03, 2.05440487e-03, 1.74924797e-03,
                 1.41095036e-03, 1.03563983e-03, 6.18913017e-04, 1.55751771e-04,
                 -3.59577455e-04, -9.33641351e-04, -1.57398027e-03, -2.28927537e-03,
                 -3.08954774e-03, -3.98639706e-03, -4.99328628e-03, -6.12588506e-03,
                 -7.40248007e-03, -8.84447046e-03, -1.04769617e-02, -1.23294782e-02,
                 -1.44368185e-02, -1.68400705e-02, -1.95878126e-02, -2.27375090e-02,
                 -2.63571208e-02, -3.05268594e-02, -3.53410537e-02, -4.09098980e-02,
                 -4.73607483e-02, -5.48383481e-02, -6.35028928e-02, -7.35242785e-02,
                 -8.50699759e-02, -9.82830774e-02, -1.13246343e-01, -1.29928723e-01,
                 -1.48114308e-01, -1.67322516e-01, -1.86743451e-01, -2.05229939e-01,
                 -2.21393962e-01, -2.33829856e-01, -2.41422319e-01, -2.43626087e-01,
                 -2.40589379e-01, -2.33066507e-01, -2.22176395e-01, -2.09126142e-01,
                 -1.94999564e-01, -1.80648062e-01, -1.66669072e-01, -1.53436754e-01,
                 -1.41152937e-01, -1.29898382e-01, -1.19675306e-01, -1.10438998e-01,
                 -1.02119643e-01, -9.46365163e-02, -8.79067413e-02, -8.18503449e-02,
                 -7.63929257e-02, -7.14668440e-02, -6.70115059e-02, -6.29731544e-02,
                 -5.93043904e-02, -5.59635737e-02, -5.29142085e-02, -5.01243290e-02,
                 -4.75659395e-02, -4.52145021e-02, -4.30484918e-02, -4.10489919e-02,
                 -3.91993555e-02, -3.74849007e-02, -3.58926561e-02, -3.44111353e-02,
                 -3.30301486e-02, -3.17406333e-02, -3.05345154e-02, -2.94045828e-02,
                 -2.83443830e-02, -2.73481274e-02, -2.64106173e-02, -2.55271695e-02,
                 -2.46935589e-02, -2.39059686e-02, -2.31609409e-02, -2.24553374e-02,
                 -2.17863068e-02, -2.11512545e-02, -2.05478122e-02, -1.99738174e-02,
                 -1.94272927e-02, -1.89064239e-02, -1.84095477e-02, -1.79351364e-02,
                 -1.74817816e-02, -1.70481867e-02, -1.66331555e-02, -1.62355815e-02,
                 -1.58544424e-02, -1.54887893e-02, -1.51377436e-02, -1.48004894e-02,
                 -1.44762679e-02, -1.41643732e-02, -1.38641463e-02, -1.35749755e-02,
                 -1.32962863e-02, -1.30275450e-02, -1.27682506e-02, -1.25179340e-02,
                 -1.22761561e-02, -1.20425050e-02, -1.18165945e-02, -1.15980609e-02,
                 -1.13865621e-02, -1.11817777e-02, -1.09834038e-02, -1.07911551e-02,
                 -1.06047623e-02, -1.04239722e-02, -1.02485437e-02, -1.00782497e-02,
                 -9.91287650e-03, -9.75222007e-03, -9.59608797e-03, -9.44429744e-03,
                 -9.29667656e-03, -9.15306006e-03, -9.01329238e-03, -8.87722519e-03,
                 -8.74471747e-03, -8.61563577e-03, -8.48985255e-03, -8.36724568e-03,
                 -8.24770006e-03]), ([-0.02231422, -0.02258234, -0.02285628, -0.02313624, -0.02342241,
                                           -0.02371501, -0.02401424, -0.02432033, -0.02463352, -0.02495406,
                                           -0.0252822, -0.02561821, -0.02596238, -0.026315, -0.02667638,
                                           -0.02704686, -0.02742676, -0.02781646, -0.02821632, -0.02862675,
                                           -0.02904816, -0.02948099, -0.0299257, -0.03038279, -0.03085275,
                                           -0.03133614, -0.03183353, -0.03234552, -0.03287276, -0.03341591,
                                           -0.03397569, -0.03455285, -0.03514822, -0.03576263, -0.03639698,
                                           -0.03705225, -0.03772945, -0.03842968, -0.03915408, -0.0399039,
                                           -0.04068045, -0.04148514, -0.04231947, -0.04318506, -0.04408361,
                                           -0.04501698, -0.04598713, -0.0469962, -0.04804647, -0.04914037,
                                           -0.05028055, -0.05146984, -0.05271131, -0.05400824, -0.05536421,
                                           -0.05678304, -0.0582689, -0.05982625, -0.06145996, -0.06317524,
                                           -0.06497777, -0.06687365, -0.06886947, -0.07097232, -0.07318982,
                                           -0.07553015, -0.07800201, -0.08061463, -0.08337771, -0.08630134,
                                           -0.08939579, -0.09267135, -0.09613787, -0.0998042, -0.10367743,
                                           -0.10776161, -0.11205608, -0.11655305, -0.12123419, -0.1260659,
                                           -0.1309928, -0.135929, -0.14074653, -0.14526074, -0.14921288,
                                           -0.15225127, -0.1539152, -0.15362918, -0.15072062, -0.1444781,
                                           -0.13426608, -0.11969626, -0.10082225, -0.07828195, -0.05329558,
                                           -0.02747288, -0.00248199, 0.02028539, 0.03992285, 0.05604571,
                                           0.06869596, 0.07819269, 0.08499061, 0.08957637, 0.09240641,
                                           0.09387743, 0.09431796, 0.09399139, 0.09310427, 0.09181606,
                                           0.09024844, 0.08849346, 0.08662021, 0.08468018, 0.08271145,
                                           0.08074195, 0.07879188, 0.07687566, 0.07500334, 0.07318168,
                                           0.07141499, 0.06970574, 0.06805506, 0.06646307, 0.06492917,
                                           0.06345225, 0.06203081, 0.06066314, 0.05934736, 0.05808149,
                                           0.05686351, 0.05569141, 0.0545632, 0.05347693, 0.0524307,
                                           0.05142268, 0.0504511, 0.04951428, 0.04861061, 0.04773856,
                                           0.04689665, 0.0460835, 0.04529779, 0.04453826, 0.04380373,
                                           0.04309307, 0.04240522, 0.04173916, 0.04109394, 0.04046865,
                                           0.03986242, 0.03927446, 0.03870397, 0.03815024, 0.03761256,
                                           0.03709027, 0.03658276, 0.03608943, 0.03560971, 0.03514307,
                                           0.03468899, 0.034247, 0.03381663, 0.03339744, 0.03298902,
                                           0.03259097, 0.03220291, 0.03182447, 0.03145531, 0.03109511,
                                           0.03074355, 0.03040033, 0.03006515, 0.02973776, 0.02941788,
                                           0.02910527, 0.02879968, 0.02850089, 0.02820867, 0.02792282,
                                           0.02764312, 0.0273694, 0.02710146, 0.02683913, 0.02658222,
                                           0.02633059, 0.02608406, 0.0258425, 0.02560574]),
          ([4.49293591e-03, 4.50881086e-03, 4.52446195e-03, 4.53979808e-03,
                 4.55485048e-03, 4.56952601e-03, 4.58384847e-03, 4.59772249e-03,
                 4.61116305e-03, 4.62407230e-03, 4.63645479e-03, 4.64820986e-03,
                 4.65932977e-03, 4.66971064e-03, 4.67933019e-03, 4.68808081e-03,
                 4.69592305e-03, 4.70274492e-03, 4.70848665e-03, 4.71303106e-03,
                 4.71629430e-03, 4.71815296e-03, 4.71849464e-03, 4.71718833e-03,
                 4.71408773e-03, 4.70905252e-03, 4.70189597e-03, 4.69246628e-03,
                 4.68052845e-03, 4.66591632e-03, 4.64833705e-03, 4.62760651e-03,
                 4.60336230e-03, 4.57539755e-03, 4.54326591e-03, 4.50673163e-03,
                 4.46524656e-03, 4.41853806e-03, 4.36593402e-03, 4.30711430e-03,
                 4.24125508e-03, 4.16797481e-03, 4.08626297e-03, 3.99565812e-03,
                 3.89491856e-03, 3.78347835e-03, 3.65980771e-03, 3.52320313e-03,
                 3.37177340e-03, 3.20463275e-03, 3.01943301e-03, 2.81504536e-03,
                 2.58853932e-03, 2.33845963e-03, 2.06112724e-03, 1.75464526e-03,
                 1.41436345e-03, 1.03778266e-03, 6.18980337e-04, 1.54629160e-04,
                 -3.62877625e-04, -9.38015922e-04, -1.58064613e-03, -2.29685132e-03,
                 -3.09954133e-03, -3.99706798e-03, -5.00651395e-03, -6.13946092e-03,
                 -7.41876397e-03, -8.86063671e-03, -1.04959973e-02, -1.23477353e-02,
                 -1.44581129e-02, -1.68596459e-02, -1.96105914e-02, -2.27572317e-02,
                 -2.63802054e-02, -3.05449859e-02, -3.53626897e-02, -4.09239060e-02,
                 -4.73784268e-02, -5.48447605e-02, -6.35132622e-02, -7.35187282e-02,
                 -8.50691458e-02, -9.82612000e-02, -1.13231244e-01, -1.29888846e-01,
                 -1.48085885e-01, -1.67270687e-01, -1.86710885e-01, -2.05183782e-01,
                 -2.21373897e-01, -2.33811080e-01, -2.41426000e-01, -2.43640456e-01,
                 -2.40609265e-01, -2.33096785e-01, -2.22193502e-01, -2.09149990e-01,
                 -1.95000648e-01, -1.80654043e-01, -1.66651780e-01, -1.53424425e-01,
                 -1.41121190e-01, -1.29872234e-01, -1.19634465e-01, -1.10404221e-01,
                 -1.02074293e-01, -9.45973601e-02, -8.78601962e-02, -8.18098584e-02,
                 -7.63473867e-02, -7.14270724e-02, -6.69683625e-02, -6.29354132e-02,
                 -5.92644793e-02, -5.59286802e-02, -5.28780111e-02, -5.00927738e-02,
                 -4.75337045e-02, -4.51865603e-02, -4.30203262e-02, -4.10248012e-02,
                 -3.91752758e-02, -3.74645099e-02, -3.58726247e-02, -3.43945394e-02,
                 -3.30140982e-02, -3.17277930e-02, -3.05223601e-02, -2.93954377e-02,
                 -2.83360284e-02, -2.73426069e-02, -2.64059682e-02, -2.55251977e-02,
                 -2.46925211e-02, -2.39074697e-02, -2.31634220e-02, -2.24602336e-02,
                 -2.17922203e-02, -2.11594729e-02, -2.05570752e-02, -1.99852874e-02,
                 -1.94398283e-02, -1.89210784e-02, -1.84252849e-02, -1.79529128e-02,
                 -1.75006525e-02, -1.70690259e-02, -1.66550983e-02, -1.62594281e-02,
                 -1.58793990e-02, -1.55155913e-02, -1.51656612e-02, -1.48301993e-02,
                 -1.45070964e-02, -1.41969454e-02, -1.38978398e-02, -1.36103686e-02,
                 -1.33328018e-02, -1.30657201e-02, -1.28075478e-02, -1.25588541e-02,
                 -1.23181986e-02, -1.20861367e-02, -1.18613478e-02, -1.16443719e-02,
                 -1.14339941e-02, -1.12307383e-02, -1.10334838e-02, -1.08427378e-02,
                 -1.06574633e-02, -1.04781509e-02, -1.03038387e-02, -1.01350003e-02,
                 -9.97074140e-03, -9.81151900e-03, -9.65649973e-03, -9.50612410e-03,
                 -9.35961386e-03, -9.21739354e-03, -9.07873483e-03, -8.94404676e-03,
                 -8.81264642e-03, -8.68492784e-03, -8.56024950e-03, -8.43899099e-03,
                 -8.32054860e-03]), ([-0.02234004, -0.02260785, -0.02288202, -0.02316166, -0.02344807,
                                           -0.02374032, -0.0240398, -0.02434553, -0.02465897, -0.02497912,
                                           -0.02530752, -0.02564312, -0.02598756, -0.02633974, -0.0267014,
                                           -0.0270714, -0.02745159, -0.02784079, -0.02824094, -0.02865084,
                                           -0.02907254, -0.02950481, -0.02994983, -0.0304063, -0.03087659,
                                           -0.03135933, -0.03185704, -0.03236834, -0.03289591, -0.03343831,
                                           -0.03399844, -0.0345748, -0.03517053, -0.03578407, -0.0364188,
                                           -0.03707313, -0.03775072, -0.03844993, -0.03917474, -0.03992346,
                                           -0.04070043, -0.04150392, -0.04233869, -0.04320297, -0.04410197,
                                           -0.04503392, -0.04600454, -0.04701206, -0.0480628, -0.049155,
                                           -0.05029567, -0.05148308, -0.05272507, -0.05401992, -0.05537642,
                                           -0.05679294, -0.05827934, -0.05983412, -0.06146839, -0.06318079,
                                           -0.0649839, -0.06687654, -0.06887294, -0.07097215, -0.07319023,
                                           -0.07552644, -0.07799888, -0.08060682, -0.08337047, -0.08628877,
                                           -0.08938378, -0.09265329, -0.09612032, -0.09977979, -0.10365351,
                                           -0.10772997, -0.11202493, -0.11651338, -0.12119508, -0.12601773,
                                           -0.13094542, -0.13587272, -0.14069157, -0.14519853, -0.14915303,
                                           -0.15218849, -0.15385631, -0.15357557, -0.15067189, -0.14444629,
                                           -0.13423637, -0.11969357, -0.10081063, -0.07829804, -0.05328559,
                                           -0.02748145, -0.00245389, 0.02030412, 0.03997404, 0.05609093,
                                           0.06876086, 0.07825159, 0.08505708, 0.08963662, 0.09246634,
                                           0.09393163, 0.09436777, 0.09403639, 0.09314323, 0.09185126,
                                           0.09027723, 0.08851944, 0.08664003, 0.08469797, 0.08272359,
                                           0.08075268, 0.07879753, 0.07688038, 0.07500354, 0.07318129,
                                           0.0714106, 0.06970103, 0.06804681, 0.06645469, 0.06491766,
                                           0.06344075, 0.06201653, 0.06064898, 0.05933071, 0.05806503,
                                           0.05684483, 0.05567299, 0.05454278, 0.05345679, 0.05240876,
                                           0.05140105, 0.05042784, 0.04949136, 0.04858621, 0.04771449,
                                           0.04687124, 0.04605843, 0.04527149, 0.04451231, 0.04377664,
                                           0.04306633, 0.04237744, 0.04171172, 0.04106554, 0.04044059,
                                           0.03983348, 0.03924584, 0.03867454, 0.03812113, 0.03758269,
                                           0.03706072, 0.0365525, 0.03605948, 0.0355791, 0.03511276,
                                           0.03465807, 0.03421637, 0.03378542, 0.03336652, 0.03295756,
                                           0.03255979, 0.03217122, 0.03179305, 0.03142342, 0.03106349,
                                           0.03071148, 0.03036851, 0.03003292, 0.02970577, 0.0293855,
                                           0.02907313, 0.02876717, 0.02846861, 0.02817604, 0.02789042,
                                           0.0276104, 0.0273369, 0.02706865, 0.02680653, 0.02654933,
                                           0.02629791, 0.0260511, 0.02580975, 0.02557272]))]
        ,
        [110956.62850765084, 202343.42143233278, 202307.3088192582],
        [([['bruker_1601.s2p', '8170796692.508812', '54727.15518984045',
                 '0.9890383947595066', '0.03841265989075973',
                 '110956.62850765084', '0.0'],
                ['fujikura_1601.s2p', '7895290829.462796', '83700.3787612967',
                 '0.8939286535496657', '0.5235445338703292', '202343.42143233278',
                 '0.0'],
                ['fujikura_201.s2p', '7895290832.099763', '83699.84776072523',
                 '0.8937812193795419', '0.5232758509940983', '202307.3088192582',
                 '0.0']])])
"""

"""
    "Hier wird die Ausgabe in einem File gespeichert"
    "DataToSave ist dann was online angezeigt werden sollte."
    with open(filelocation + '/Q_Results.dat', 'w') as filetosave:
        filetosave.write('#FileName      f0(CircleFit) [Hz]       Ql      beta1      beta2        Q0     Data removed [%]\n')
        for data in DataToSave:
            np.savetxt(filetosave, data, delimiter="    ", fmt='%s')
    filetosave.close()
    print("Data Saved")




    "Das sind die parameter die geplottet werden sollen"
    "In der GUI kann man anklicken welche Datei man sehen moechte"
    "Waere gut wenn man das online auch machen koennte"
    "Vielleicht sogar uebereinander plotten als vergleich"
    "Ich hab hier mal einen beispiel auf dem dictionary geplottet damit du weist,"
    "wie das ungefahr auszusehen hat."

    TDict = {}
    for k in range(len(ListofFiles)):
        TDict[ListofFiles[k]] = [WCCFXList[k], PlotDataList[k]]

    Entry = TDict[ListofFiles[0]]

    #RedFreq = Entry[0][0]
    #Qloaded = Entry[0][1]
    RS21 = Entry[1][0]
    IS21 = Entry[1][1]
    WRS21 = Entry[1][2]
    WIS21 = Entry[1][3]

    plt.plot(RS21,IS21,'go', label= 'S21 input data')
    plt.plot(WRS21,WIS21,'r-', label= 'S21 fit', linewidth=3.0)
    plt.axis('equal')  #  damit die kreise auch als kreise dargestellt werden
    plt.grid()
    plt.xlabel('Re(S21)')
    plt.ylabel('Im(S21)')
    plt.legend()
    plt.show()
"""
