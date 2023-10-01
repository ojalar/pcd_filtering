import open3d as o3d
import numpy as np
import copy
import argparse

class PCDFilter:
    # class for basic filtering operations on a point cloud
    def __init__(self, pcd):
        # pcd: open3d point cloud
        # store pcd and make a copy
        self.pcd = pcd
    
    def crop(self, min_b, max_b):
        # crop the point cloud to the desired region
        bbox = o3d.geometry.AxisAlignedBoundingBox(min_b, max_b)
        self.pcd = self.pcd.crop(bbox)

    def voxel_grid_filter(self, vs):
        # perform voxel grid filtering to clear out duplicate points
        self.pcd = self.pcd.voxel_down_sample(vs)

    def ROR(self, n, r):
        # radius outlier removal to filter noise from point cloud
        self.pcd, _ = self.pcd.remove_radius_outlier(n, r)
     
    def visualize(self, zoom = 0.5):
        # visualize point cloud
        o3d.visualization.draw_geometries([self.pcd],
                front = [-0.60336580821840613, 
                    0.68006389736189432, 
                    0.41648865167961135],
			lookat = [5.0921835017702852, 
                -6.6328737715031316, 
                32.18737291561505],
			up = [0.71506868395318912, 
                0.23017763734166954, 
                0.6600719903898824],
			zoom = zoom)

    def get_number_of_points(self):
        # return number of points in point cloud
        return len(self.pcd.points)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path', help='Path to point cloud file', required=True)
    args = vars(parser.parse_args())
    # load point cloud from file
    pcd = o3d.io.read_point_cloud(args["path"])
    
    # initialise filter
    pcdf = PCDFilter(pcd)
    
    # visualize before any operations
    pcdf.visualize(zoom=0.16)
   
    # crop point cloud with defined boundaries
    min_b = (0, -10, 30)
    max_b = (10, 10, 40)
    pcdf.crop(min_b, max_b)
    pcdf.visualize(zoom=0.60)
    
    # voxel grid filtering
    print("Number of points in cloud BEFORE voxel grid filter:", 
            pcdf.get_number_of_points())
    vs = 1e-2
    pcdf.voxel_grid_filter(vs)
    print("Number of points in cloud AFTER voxel grid filter:", 
            pcdf.get_number_of_points())
    pcdf.visualize(zoom=0.60)

    # radius outlier removal
    n = 50
    r = 5e-2
    pcdf.ROR(n, r)
    pcdf.visualize(zoom=0.60)
    
