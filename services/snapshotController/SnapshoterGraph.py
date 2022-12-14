import png
import os
from loguru import logger 
from typing import List

from entity_types import Coords
from settings import SNAPSHOTS_DIR, SNAPSHOT_FILE_NAME, SNAPSHOTS_WIDTH, SNAPSHOTS_HEIGHT


logger.add("logs/info.log", format="{time} | {level} | {message}", level="INFO", compression="zip", rotation="50 KB")


class SnapshoterGraph:
	# :shema - list of str. Each of str - line(row) '1' or '0'
	# '1' is white pixel, '0' is black pixel on snapshot

	def __init__(self):
		self.snapshot_name_suffix = self.__get_snapshot_name_suffix()


	def create_black_white_snapshot(self, point_list:List[Coords]):
		# The store_of_pixels_value - black_white value list on besided shema.
		# Just transform str to list of int.
		# For a color mode the list would be little difficult
		shema = self.__point_list_to_shema(point_list)
		store_of_pixels_value = [[int(c) for c in row] for row in shema]
		self.__create_png(store_of_pixels_value)


	def __point_list_to_shema(self, point_list:List[Coords])->List[str]:
		# In this method we will create shema for black_white mode create_png.
		width = SNAPSHOTS_WIDTH
		higth = SNAPSHOTS_HEIGHT

		shema = ['1'*width]*higth

		for x, y in point_list:
			if x < 0 or y < 0:
				continue
			if y < higth:
				shema[higth-y-1] = shema[higth-y-1][:x-1]+"0"+shema[higth-y-1][x:]
		return shema


	def __create_png(self, store_of_pixels_value:List[List[int]], mode:str="black_white"):
		height = len(store_of_pixels_value)
		file_path = SNAPSHOTS_DIR + "/" + SNAPSHOT_FILE_NAME + str(self.snapshot_name_suffix) + ".png"

		if mode == 'black_white':
			width = len(store_of_pixels_value[0])
			with open(file_path, 'wb') as f: 
				w = png.Writer(width, height, greyscale=True, bitdepth=1)
				w.write(f, store_of_pixels_value)
		elif mode == 'color':
			width = len(store_of_pixels_value[0]) // 3	
			with open(file_path, 'wb') as f: 
				w = png.Writer(width, height, greyscale=False)
				w.write(f, store_of_pixels_value)
		logger.info("A photo has just been taken with mode - black_white and path: "+file_path)
		self.snapshot_name_suffix += 1 # We change it for further snapshot on current session


	def __get_snapshot_name_suffix(self)->int:
		# Create uniqe suffix for each file.png
		return len(os.listdir(SNAPSHOTS_DIR))





if __name__ == '__main__':
	s = SnapshoterGraph()
	

	data = [(1, -1), (2, 5), (3, 7), (4, 9), (5, 10), (6, 13), (7, 14), (8, 18), (9, 19), (10, 23), (11, 25), (12, 28), (13, 30), (14, 32), (15, 37), (16, 39), (17, 42), (18, 45), (19, 48), (20, 51), (21, 54), (22, 56), (23, 59), (24, 63), (25, 66), (26, 70), (27, 72), (28, 75), (29, 79), (30, 83), (31, 85), (32, 89), (33, 91), (34, 95), (35, 99), (36, 102), (37, 106), (38, 109), (39, 113), (40, 116), (41, 120), (42, 123), (43, 126), (44, 130), (45, 133), (46, 136), (47, 141), (48, 144), (49, 147), (50, 152), (51, 155), (52, 158), (53, 161), (54, 166), (55, 170), (56, 173), (57, 177), (58, 180), (59, 185), (60, 189), (61, 192), (62, 196), (63, 199), (64, 203), (65, 207), (66, 211), (67, 214), (68, 218), (69, 222), (70, 226), (71, 230), (72, 234), (73, 238), (74, 242), (75, 246), (76, 250), (77, 254), (78, 258), (79, 262), (80, 265), (81, 269), (82, 273), (83, 277), (84, 282), (85, 286), (86, 289), (87, 293), (88, 298), (89, 302), (90, 305), (91, 309), (92, 314), (93, 318), (94, 322), (95, 326), (96, 331), (97, 334), (98, 338), (99, 343), (100, 346), (101, 351), (102, 356), (103, 359), (104, 364), (105, 368), (106, 372), (107, 377), (108, 380), (109, 385), (110, 388), (111, 393), (112, 397), (113, 402), (114, 405), (115, 410), (116, 414), (117, 419), (118, 422), (119, 427), (120, 431), (121, 436), (122, 440), (123, 445), (124, 449), (125, 454), (126, 458), (127, 461), (128, 467), (129, 470), (130, 476), (131, 480), (132, 483), (133, 489), (134, 493), (135, 497), (136, 502), (137, 506), (138, 510), (139, 515), (140, 519), (141, 524), (142, 528), (143, 533), (144, 537), (145, 541), (146, 545), (147, 551), (148, 555), (149, 559), (150, 564), (151, 569), (152, 573), (153, 578), (154, 582), (155, 586), (156, 591), (157, 596), (158, 601), (159, 605), (160, 609), (161, 614), (162, 618), (163, 623), (164, 628), (165, 633), (166, 637), (167, 642), (168, 646), (169, 651), (170, 655), (171, 660), (172, 664), (173, 669), (174, 674), (175, 678), (176, 683), (177, 687), (178, 692), (179, 697), (180, 701), (181, 706), (182, 711), (183, 715), (184, 720), (185, 725), (186, 730), (187, 734), (188, 739), (189, 744), (190, 749), (191, 754), (192, 758), (193, 763), (194, 768), (195, 773), (196, 778), (197, 782), (198, 787), (199, 791), (200, 796), (201, 801), (202, 806), (203, 811), (204, 815), (205, 820), (206, 825), (207, 830), (208, 835), (209, 840), (210, 844), (211, 849), (212, 854), (213, 859), (214, 864), (215, 868), (216, 873), (217, 878), (218, 884), (219, 887), (220, 893), (221, 898), (222, 903), (223, 907), (224, 912), (225, 917), (226, 923), (227, 927), (228, 932), (229, 937), (230, 941), (231, 947), (232, 952), (233, 956), (234, 961), (235, 967), (236, 971), (237, 976), (238, 981), (239, 986), (240, 991), (241, 996), (242, 1001), (243, 1006), (244, 1011), (245, 1016), (246, 1021), (247, 1025), (248, 1031), (249, 1036), (250, 1041), (251, 1046), (252, 1050), (253, 1056), (254, 1060), (255, 1066), (256, 1071), (257, 1076), (258, 1081), (259, 1086), (260, 1091), (261, 1096), (262, 1101), (263, 1106), (264, 1111), (265, 1116), (266, 1121), (267, 1126), (268, 1132), (269, 1136), (270, 1142), (271, 1146), (272, 1152), (273, 1157), (274, 1162), (275, 1167), (276, 1173), (277, 1177), (278, 1182), (279, 1187), (280, 1192), (281, 1198), (282, 1202), (283, 1208), (284, 1213), (285, 1218), (286, 1223), (287, 1228), (288, 1234), (289, 1239), (290, 1243), (291, 1249), (292, 1254), (293, 1260), (294, 1264), (295, 1269), (296, 1275), (297, 1280), (298, 1285), (299, 1291), (300, 1295), (301, 1300), (302, 1306), (303, 1311), (304, 1316), (305, 1322), (306, 1327), (307, 1331), (308, 1337), (309, 1342), (310, 1347), (311, 1352), (312, 1358), (313, 1363), (314, 1368), (315, 1374), (316, 1379), (317, 1384), (318, 1389), (319, 1395), (320, 1400), (321, 1405), (322, 1410), (323, 1416), (324, 1421), (325, 1426), (326, 1431), (327, 1436), (328, 1442), (329, 1447), (330, 1452), (331, 1457), (332, 1462), (333, 1469), (334, 1474), (335, 1479), (336, 1484), (337, 1489), (338, 1494), (339, 1500), (340, 1505), (341, 1511), (342, 1516), (343, 1521), (344, 1526), (345, 1532), (346, 1538), (347, 1543), (348, 1548), (349, 1553), (350, 1558), (351, 1564), (352, 1569), (353, 1574), (354, 1580), (355, 1586), (356, 1591), (357, 1596), (358, 1601), (359, 1607), (360, 1612), (361, 1617), (362, 1623), (363, 1628), (364, 1633), (365, 1639), (366, 1644), (367, 1650), (368, 1656), (369, 1661), (370, 1666), (371, 1672), (372, 1677), (373, 1683), (374, 1688), (375, 1693), (376, 1699), (377, 1704), (378, 1710), (379, 1715), (380, 1720), (381, 1726), (382, 1731), (383, 1737), (384, 1742), (385, 1748), (386, 1753), (387, 1759), (388, 1764), (389, 1770), (390, 1774), (391, 1780), (392, 1785), (393, 1791), (394, 1796), (395, 1802), (396, 1807), (397, 1813), (398, 1818), (399, 1824), (400, 1830), (401, 1835), (402, 1841), (403, 1846), (404, 1851), (405, 1856), (406, 1862), (407, 1868), (408, 1873), (409, 1879), (410, 1885), (411, 1890), (412, 1896), (413, 1900), (414, 1906), (415, 1912), (416, 1918), (417, 1923), (418, 1929), (419, 1935), (420, 1939), (421, 1945), (422, 1951), (423, 1956), (424, 1962), (425, 1968), (426, 1973), (427, 1978), (428, 1984), (429, 1990), (430, 1996), (431, 2000), (432, 2006), (433, 2012), (434, 2018), (435, 2024), (436, 2028), (437, 2034), (438, 2040), (439, 2046), (440, 2051), (441, 2056), (442, 2062), (443, 2068), (444, 2073), (445, 2079), (446, 2085), (447, 2091), (448, 2095), (449, 2101)]
	s.create_black_white_snapshot(data)