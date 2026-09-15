import numpy as np

class Rectangle:
    def __init__(self, center, u_axis, v_axis, width, height):
        """
        center: [x, y, z] center of rectangle
        u_axis: vector defining width direction
        v_axis: vector defining height direction
        width, height: scalar dimensions
        """
        self.center = np.array(center, dtype=float)
        self.u = np.array(u_axis, dtype=float) / np.linalg.norm(u_axis)
        self.v = np.array(v_axis, dtype=float) / np.linalg.norm(v_axis)
        
        # Normal vector perpendicular to the rectangle plane
        normal = np.cross(self.u, self.v)
        self.normal = normal / np.linalg.norm(normal)
        
        self.width = float(width)
        self.height = float(height)
        self.area = self.width * self.height

    def sample_points(self, n):
        """Generates n uniform random points on the rectangle surface."""
        u_rand = np.random.uniform(-self.width / 2.0, self.width / 2.0, n)
        v_rand = np.random.uniform(-self.height / 2.0, self.height / 2.0, n)
        return self.center + u_rand[:, None] * self.u + v_rand[:, None] * self.v

def calculate_etendue_3_rectangles(r1, r2, r3, n_samples=1_000_000):
    """
    Calculates A * Omega (Etendue) for particles hitting R1, R2, and R3.
    Returns (G, standard_error) in units of Area * Steradians.
    """
    # 1. Uniformly sample points on R1 and R2
    p1 = r1.sample_points(n_samples)
    p2 = r2.sample_points(n_samples)
    
    # 2. Compute ray vectors, distances, and unit directions
    disp = p2 - p1
    dist = np.linalg.norm(disp, axis=1)
    d = disp / dist[:, None]
    
    # 3. Angles between ray and surface normals
    cos1 = np.abs(np.dot(d, r1.normal))
    cos2 = np.abs(np.dot(d, r2.normal))
    
    # 4. Ray-plane intersection test with R3
    denom = np.dot(d, r3.normal)
    valid_denom = np.abs(denom) > 1e-10
    
    t = np.zeros(n_samples)
    t[valid_denom] = np.dot(r3.center - p1[valid_denom], r3.normal) / denom[valid_denom]
    
    # Intersection point P_hit = P1 + t * d
    p_hit = p1 + t[:, None] * d
    hit_disp = p_hit - r3.center
    
    # Project hit point onto R3 local axes
    u_proj = np.abs(np.dot(hit_disp, r3.u))
    v_proj = np.abs(np.dot(hit_disp, r3.v))
    
    # Ray hits R3 if t > 0 and point is within bounds
    hits_r3 = valid_denom & (t > 0) & (u_proj <= r3.width / 2.0) & (v_proj <= r3.height / 2.0)
    
    # 5. Differential throughput integration weight: (cos theta_1 * cos theta_2) / r^2
    weights = np.zeros(n_samples)
    weights[hits_r3] = (cos1[hits_r3] * cos2[hits_r3]) / (dist[hits_r3] ** 2)
    
    # Monte Carlo integral G = (A1 * A2) * E[weights]
    g_mean = (r1.area * r2.area) * np.mean(weights)
    g_std_err = (r1.area * r2.area) * np.std(weights) / np.sqrt(n_samples)
    
    return g_mean, g_std_err

def calculate_etendue_2_rectangles(r1, r2, n_samples=1_000_000):
    """
    Calculates A * Omega (Etendue) between two rectangles R1 and R2.
    Returns (G, standard_error) in units of Area * Steradians.
    """
    # 1. Uniformly sample points on R1 and R2
    p1 = r1.sample_points(n_samples)
    p2 = r2.sample_points(n_samples)
    
    # 2. Compute ray vectors, distances, and unit directions
    disp = p2 - p1
    dist = np.linalg.norm(disp, axis=1)
    d = disp / dist[:, None]
    
    # 3. Angles between ray and surface normals
    cos1 = np.abs(np.dot(d, r1.normal))
    cos2 = np.abs(np.dot(d, r2.normal))
    
    # 4. Differential throughput integration weight: (cos theta_1 * cos theta_2) / r^2
    weights = (cos1 * cos2) / (dist ** 2)
    
    # Monte Carlo integral G = (A1 * A2) * E[weights]
    g_mean = (r1.area * r2.area) * np.mean(weights)
    g_std_err = (r1.area * r2.area) * np.std(weights) / np.sqrt(n_samples)
    
    return g_mean, g_std_err

# --- Example Usage ---
if __name__ == "__main__":
    # Define 2 parallel rectangles separated by 5 units along Z-axis
    rect1 = Rectangle(center=[0, 0, 0], u_axis=[1, 0, 0], v_axis=[0, 1, 0], width=80, height=30)
    rect2 = Rectangle(center=[0, 0, 10.2], u_axis=[1, 0, 0], v_axis=[0, 1, 0], width=80, height=30)

    G, error = calculate_etendue_2_rectangles(rect1, rect2, n_samples=2_000_000)
    
    print(f"Steradian × Area (G): {G:.6e} m²·sr")
    print(f"Standard Error:      ±{error:.6e} m²·sr")



# # --- Example Usage ---
# if __name__ == "__main__":
#     # Define 3 coaxial rectangles separated along Z-axis
#     rect1 = Rectangle(center=[0, 0, 0],   u_axis=[1, 0, 0], v_axis=[0, 1, 0], width=80, height=30)
#     rect2 = Rectangle(center=[0, 0, 12.8],   u_axis=[1, 0, 0], v_axis=[0, 1, 0], width=80, height=30)
#     rect3 = Rectangle(center=[0, 0, 23],  u_axis=[1, 0, 0], v_axis=[0, 1, 0], width=80, height=30)

#     G, error = calculate_etendue_3_rectangles(rect1, rect2, rect3, n_samples=2_000_000)
    
#     print(f"Steradian × Area (G): {G:.6e} m²·sr")
#     print(f"Standard Error:      ±{error:.6e} m²·sr")