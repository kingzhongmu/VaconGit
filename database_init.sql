SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `mock_config`
-- ----------------------------
DROP TABLE IF EXISTS `mock_data`;
CREATE TABLE `mock_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT = 1000000,
  `project_name` varchar(50) DEFAULT NULL,
  `test_page` varchar(50) DEFAULT NULL,
  `test_point` varchar(50) DEFAULT NULL,
  `route_url` varchar(50) DEFAULT NULL,
  `method` varchar(5) DEFAULT NULL,
  `req_para` varchar(100) DEFAULT NULL,
  `req_data` varchar(100) DEFAULT NULL,
  `res_data` varchar(1000) DEFAULT NULL,
  `test_detail_des` varchar(50) DEFAULT NULL,
  `current_active` int(1) DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of mock_config
-- ----------------------------
INSERT INTO `mock_data` VALUES (
1000001,
'博物官',
'首页测试',
'首页类型-导览',
'api/getHomeRecommendV2',
'post',
'req_para',
'req_data',
'res_data',
'test_detail_des',
1,
'2017-9-18 13:16:17');
