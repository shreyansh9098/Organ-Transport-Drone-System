import random
import math
from typing import List, Tuple, Dict

class RouteOptimizer:
    """Mock AI route optimization module"""
    
    NO_FLY_ZONES = [
        {"lat": 40.7580, "lon": -73.9855, "radius_km": 5},
        {"lat": 34.0522, "lon": -118.2437, "radius_km": 8},
        {"lat": 41.8781, "lon": -87.6298, "radius_km": 6},
    ]
    
    WEATHER_CONDITIONS = {
        "clear": {"score": 1.0, "speed_factor": 1.0},
        "cloudy": {"score": 0.9, "speed_factor": 0.95},
        "rain": {"score": 0.6, "speed_factor": 0.8},
        "storm": {"score": 0.3, "speed_factor": 0.6},
        "fog": {"score": 0.5, "speed_factor": 0.7},
    }
    
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers"""
        R = 6371
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    @staticmethod
    def is_in_no_fly_zone(lat: float, lon: float) -> bool:
        """Check if coordinates are in a no-fly zone"""
        for zone in RouteOptimizer.NO_FLY_ZONES:
            distance = RouteOptimizer.haversine_distance(lat, lon, zone["lat"], zone["lon"])
            if distance < zone["radius_km"]:
                return True
        return False
    
    @staticmethod
    def generate_waypoints(
        origin_lat: float,
        origin_lon: float,
        dest_lat: float,
        dest_lon: float,
        num_waypoints: int = 5
    ) -> List[Tuple[float, float]]:
        """Generate waypoints between origin and destination"""
        waypoints = [(origin_lat, origin_lon)]
        
        for i in range(1, num_waypoints):
            ratio = i / num_waypoints
            lat = origin_lat + (dest_lat - origin_lat) * ratio
            lon = origin_lon + (dest_lon - origin_lon) * ratio
            
            offset_lat = random.uniform(-0.01, 0.01)
            offset_lon = random.uniform(-0.01, 0.01)
            
            adjusted_lat = lat + offset_lat
            adjusted_lon = lon + offset_lon
            
            if not RouteOptimizer.is_in_no_fly_zone(adjusted_lat, adjusted_lon):
                waypoints.append((adjusted_lat, adjusted_lon))
            else:
                waypoints.append((lat, lon))
        
        waypoints.append((dest_lat, dest_lon))
        return waypoints
    
    @staticmethod
    def optimize_route(
        origin_lat: float,
        origin_lon: float,
        dest_lat: float,
        dest_lon: float,
        priority_level: int = 1,
        weather_condition: str = "clear"
    ) -> Dict:
        """
        Optimize route considering weather, no-fly zones, and emergency priority
        Returns optimized route with safety and weather scores
        """
        base_distance = RouteOptimizer.haversine_distance(
            origin_lat, origin_lon, dest_lat, dest_lon
        )
        
        num_waypoints = 5 if priority_level >= 3 else 8
        
        waypoints = RouteOptimizer.generate_waypoints(
            origin_lat, origin_lon, dest_lat, dest_lon, num_waypoints
        )
        
        total_distance = 0
        for i in range(len(waypoints) - 1):
            segment_dist = RouteOptimizer.haversine_distance(
                waypoints[i][0], waypoints[i][1],
                waypoints[i+1][0], waypoints[i+1][1]
            )
            total_distance += segment_dist
        
        weather_info = RouteOptimizer.WEATHER_CONDITIONS.get(
            weather_condition, RouteOptimizer.WEATHER_CONDITIONS["clear"]
        )
        weather_score = weather_info["score"]
        speed_factor = weather_info["speed_factor"]
        
        safety_score = 0.95 - (0.05 * len([w for w in waypoints if RouteOptimizer.is_in_no_fly_zone(w[0], w[1])]))
        safety_score = max(0.5, min(1.0, safety_score))
        
        avg_speed_kmh = 80 * speed_factor
        if priority_level >= 3:
            avg_speed_kmh *= 1.2
        
        estimated_time_minutes = (total_distance / avg_speed_kmh) * 60
        
        return {
            "route": [[w[0], w[1]] for w in waypoints],
            "distance_km": round(total_distance, 2),
            "estimated_time_minutes": round(estimated_time_minutes, 2),
            "weather_score": round(weather_score, 2),
            "safety_score": round(safety_score, 2),
            "optimized": True,
            "priority_level": priority_level,
            "weather_condition": weather_condition
        }
