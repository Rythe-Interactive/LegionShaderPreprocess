#version 450 
#define VERTEX_SHADER
#if defined(VERTEX_SHADER)
layout(location=SV_POSITION) in vec3 vertex;
layout(location=SV_NORMAL) in vec3 normal;
layout(location=SV_TANGENT) in vec3 tangent;
layout(location=SV_TEXCOORD0) in vec2 uv;
layout(location=SV_MODELMATRIX) in mat4 modelMatrix;
#endif
struct Camera
{
mat4 viewMatrix;
mat4 projectionMatrix;
vec3 position;
uint index;
vec3 viewDirection;
vec3 toView;
}
uniform CameraInput : SV_VIEW
{
mat4 viewMatrix;
mat4 projectionMatrix;
vec3 position;
uint index;
vec3 viewDirection;
} camera_input;
Camera InitCamera(vec3 worldPosition)
{
Camera camera;
camera.viewMatrix = camera_input.viewMatrix;
camera.projectionMatrix = camera_input.projectionMatrix;
camera.position = camera_input.position;
camera.index = camera_input.index;
camera.viewDirection = camera_input.viewDirection;
camera.toView = camera_input.position - worldPosition;
}
vec3 GetWorldPosition()
{
return (modelMatrix * vec4(vertex, 1.0)).xyz
}
vec3 GetWorldNormal()
{
return normalize((modelMatrix * vec4(normal, 0.0)).xyz);
}
vec3 GetWorldTangent()
{
vec3 worldNormal = GetWorldNormal();
vec3 worldTangent = normalize((modelMatrix * vec4(tangent, 0.0)).xyz);
return normalize(worldTangent - dot(worldTangent, worldNormal) * worldNormal);
}
vec3 GetWorldTangent(vec3 worldNormal)
{
vec3 worldTangent = normalize((modelMatrix * vec4(tangent, 0.0)).xyz);
return normalize(worldTangent - dot(worldTangent, worldNormal) * worldNormal);
}
vec3 GetWorldBitangent()
{
vec3 worldNormal = GetWorldNormal();
vec3 worldTangent = GetWorldTangent(worldNormal);
return normalize(cross(worldNormal, worldTangent));
}
vec3 GetWorldBitangent(vec3 worldNormal)
{
vec3 worldTangent = GetWorldTangent(worldNormal);
return normalize(cross(worldNormal, worldTangent));
}
vec3 GetWorldBitangent(vec3 worldNormal, vec3 worldTangent)
{
return normalize(cross(worldNormal, worldTangent));
}
vec3 GetWorldDirection(vec3 dir)
{
return normalize((modelMatrix * vec4(dir, 0.0)).xyz);
}
vec3 GetWorldPoint(vec3 p)
{
return (modelMatrix * vec4(p, 1.0)).xyz
}
mat3 GetTBN()
{
vec3 worldNormal = GetWorldNormal();
vec3 worldTangent = GetWorldTangent(worldNormal);
vec3 worldBitangent = GetWorldBitangent(worldNormal, worldTangent);
tbnMatrix = mat3(worldTangent, worldBitangent, worldNormal);
}
mat3 GetTBN(vec3 worldNormal, vec3 worldTangent)
{
vec3 orthogonalizedTangent = normalize(worldTangent - dot(worldTangent, worldNormal) * worldNormal);
vec3 worldBitangent = GetWorldBitangent(worldNormal, orthogonalizedTangent);
tbnMatrix = mat3(orthogonalizedTangent, worldBitangent, worldNormal);
}
#pragma once
#define ENUM uint
#define point_light 0
#define directional_light 1
#define spot_light 2
struct Light
{
ENUM type;			// 4	0
float attenuation;	// 4	4
float intensity;	// 4	8
uint index;			// 4	12
vec3 direction;		// 12	16
float falloff;		// 4	28
vec3 position;		// 12	32
float angle;		// 4	44
vec3 colour;		// 12	48
float meta2;		// 4	60
};
struct Material
{
vec4 albedo;
vec3 normal;
float metallic;
vec3 emissive;
float roughness;
float dielectric;
float ambientOcclusion;
float F0;
}
#pragma once
#define epsilon 0.00001
#define pi 3.141592653589793
float sum(vec2 v)
{
return v.x + v.y;
}
float sum(vec3 v)
{
return v.x + v.y + v.z;
}
float sum(vec4 v)
{
return v.x + v.y + v.z + v.w;
}
float length2(vec2 v)
{
return sum(v*v);
}
float length2(vec3 v)
{
return sum(v*v);
}
float length2(vec4 v)
{
return sum(v*v);
}
float dot01(vec2 a, vec2 b)
{
return max(dot(a, b), 0.0)
}
float dot01(vec3 a, vec3 b)
{
return max(dot(a, b), 0.0)
}
float dot01(vec4 a, vec4 b)
{
return max(dot(a, b), 0.0)
}
float clamp01(float v)
{
return clamp(v, 0, 1);
}
vec2 clamp01(vec2 v)
{
return clamp(v, 0, 1);
}
vec3 clamp01(vec3 v)
{
return clamp(v, 0, 1);
}
vec4 clamp01(vec4 v)
{
return clamp(v, 0, 1);
}
float safeDiv(float a, float b)
{
return a / max(b, epsilon);
}
vec2 safeDiv(vec2 a, float b)
{
return a / max(b, epsilon);
}
vec3 safeDiv(vec3 a, float b)
{
return a / max(b, epsilon);
}
vec4 safeDiv(vec4 a, float b)
{
return a / max(b, epsilon);
}
vec2 safeDiv(vec2 a, vec2 b)
{
return a / max(b, epsilon);
}
vec3 safeDiv(vec3 a, vec3 b)
{
return a / max(b, epsilon);
}
vec4 safeDiv(vec4 a, vec4 b)
{
return a / max(b, epsilon);
}
float Attenuation(vec3 worldPosition, vec3 lightPosition, float attenuationRadius, float lightIntensity)
{
float sqrlightDistance = length2(lightPosition - fragmentPosition);
float attenuation = pow(max(1.0 - (sqrlightDistance / (attenuationRadius * attenuationRadius)), 0.0), 2);
return attenuation * lightIntensity;
}
vec3 fresnelSchlick(float halfwayDotView, vec3 F0)
{
return F0 + (1.0 - F0) * pow(1.0 - halfwayDotView, 5.0);
}
vec3 Fresnel0(vec4 albedo, float metallic, float dielectric)
{
return mix(dielectric.xxx, albedo, metallic.xxx)
}
vec3 Fresnel0(vec4 albedo, float metallic)
{
return mix(vec3(0.04), albedo, metallic.xxx)
}
float DistributionGGX(float normalDotHalfway, float roughness)
{
float r2      = roughness * roughness;
float r4     = r2 * r2;
float NdotH2 = normalDotHalfway * normalDotHalfway;
float num   = r4;
float denom = (NdotH2 * (r4 - 1.0) + 1.0);
denom = pi * denom * denom;
return num / denom;
}
float GeometrySchlickGGX(float cosTheta, float roughness)
{
float k = (roughness * roughness) / 2.0;
float num   = cosTheta;
float denom = cosTheta * (1.0 - k) + k;
return num / denom;
}
float GeometrySmith(float normalDotView, float normalDotLight, float roughness)
{
float ggx2  = GeometrySchlickGGX(normalDotView, roughness);
float ggx1  = GeometrySchlickGGX(normalDotLight, roughness);
return ggx1 * ggx2;
}
vec3 CookTorranceBRDF(float normalDistribution, vec3 fresnelReflection, float geometryShadowing, float normalDotLight, float normalDotView)
{
return safeDiv(normalDistribution * fresnelReflection * geometryShadowing, 4.0  * normalDotLight * normalDotView);
}
vec3 LambertianDiffuse(vec3 kS, vec3 albedo, float metallic)
{
vec3 kD = (vec3(1.0) - kS) * (1.0 - metallic);
return kD * (albedo / pi);
}
float ambientIntensity;
vec3 CalculateLight(Light light, Camera camera, Material material, vec3 worldPosition, vec3 worldNormal)
{
vec3 lightDirection;
float intensity;
switch(light.type)
{
case point_light:
lightDirection = normalize(light.position - surfacePosition);
intensity = light.intensity;
break;
case directional_light:
lightDirection = light.direction;
intensity = light.intensity;
break;
case spot_light:
lightDirection = normalize(light.position - surfacePosition);
intensity = pow(max((dot(normalize(light.direction), lightDirection) - cos(light.angle*0.5)) / (1.0 - cos(light.angle*0.5)), 0.0), light.falloff) * light.intensity;
break;
default:
lightDirection = vec3(0, 1, 0);
intensity = light.intensity;
break;
}
ambientIntensity += (light.intensity * 1.5) - (intensity * 0.5);
float attenuation = Attenuation(worldPosition, light.position, light.attenuation, intensity);
if(attenuation <= 0)
return vec3(0);
vec3 radiance = lightColor * attenuation;
// Microfacet normal that will reflect the incoming light into the viewing direction.
// Technically only applies if the nanogeometry is perfectly smooth, but due to the inherent
// inaccuracy of working with fragments as the smallest size of measurement we can ignore
// nanogeometry for now.
vec3 halfwayVector = normalize(lightDirection + camera.toView);
float halfwayDotView = dot01(halfwayVector, camera.toView);
float normalDotHalfway = dot01(worldNormal, halfwayVector);
float normalDotView = dot01(worldNormal, camera.toView);
float normalDotLight = dot01(worldNormal, lightDirection);
// cook-torrance brdf
vec3 fresnelReflection = fresnelSchlick(halfwayDotView, material.F0);
float normalDistribution = DistributionGGX(normalDotHalfway, material.roughness);
float geometryShadowing = GeometrySmith(normalDotView, normalDotLight, material.roughness);
vec3 specular = CookTorranceBRDF(normalDistribution, fresnelReflection, geometryShadowing, normalDotLight, normalDotView);
vec3 diffuse = LambertianDiffuse(fresnelReflection, material.albedo.rgb, material.metallic);
return (diffuse + specular) * radiance * normalDotLight;
}
vec3 GetAmbientLight(float ambientOcclusion, vec3 albedo)
{
return (pow(ambientIntensity, 1.1) * 0.0001).xxx * ambientOcclusion.xxx * albedo;
}
#if !defined(NO_INPUT)
#pragma once
layout (std140) buffer LightsBuffer
{
Light lights[];
};
layout(std140) in MaterialInput : SV_MATERIAL
{
sampler2D albedo;
sampler2D normalHeight;
sampler2D MRDAo;
sampler2D emissive;
float heightScale;
} material_input;
#pragma once
vec2 ParallaxMap(sampler2D normalHeightMap, float scale, vec2 uv, Camera camera, mat3 tbn)
{
vec3 tangentViewDir = tbn * camera.toView;
const float minLayers = 4.0;
const float maxLayers = 32.0;
float layerCount = round(mix(maxLayers, minLayers, dot01(vec3(0.0, 0.0, 1.0), viewDir)));
float layerDepth = 1.0 / layerCount;
float currentDepth = 0.0;
float prevDepth = 0.0;
vec2 P = tangentViewDir.xy * scale;
vec2 deltaUV = P / layerCount;
vec2 currentUV = uv;
vec2 prevUV = currentUV;
float currentDepthMapValue = texture(map, currentUV).a;
float prevDepthMapValue = currentDepthMapValue;
while(currentDepth < currentDepthMapValue)
{
prevUV = currentUV;
currentUV -= deltaUV;
prevDepthMapValue = currentDepthMapValue;
currentDepthMapValue = texture(map, currentUV).a;
prevDepth = currentDepth;
currentDepth += layerDepth;
}
float afterDepth = currentDepthMapValue - currentDepth;
float beforeDepth = prevDepthMapValue - prevDepth;
return mix(prevUV, currentUV, afterDepth / (afterDepth - beforeDepth));
}
vec2 ParallaxMap(float height, float scale, vec2 uv, Camera camera, mat3 tbn)
{
vec3 tangentViewDir = tbn * camera.toView;
float offset = (height * 2.0 - 1.0) * scale * -1;
vec2 parallexOffset = (tangentViewDir.xy / tangentViewDir.z) * offset;
return uv - parallexOffset;
}
vec3 NormalMap(sampler2D map, vec2 uv, mat3 tbn)
{
return normalize(tbn * normalize(texture(map, uv).xyz * 2.0 - 1.0));
}
vec4 AlbedoMap(sampler2D albedoMap, vec2 uv)
{
return pow(texture(albedoMap, uv).rgba, vec4(vec3(2.2), 1.0));
}
vec4 LightingData(sampler2D MRDAoMap, vec2 uv)
{
return texture(MRDAoMap, uv);
}
vec3 EmissiveMap(sampler emissiveMap, vec2 uv)
{
return texture(emissiveMap, uv).rgb;
}
Material ExtractMaterial(vec2 uv, Camera camera, vec3 worldNormal, vec3 worldTangent)
{
mat3 tbn = GetTBN(worldNormal, worldTangent);
vec2 texcoords = ParallaxMap(material_input.normalHeight, material_input.heightScale, uv, camera);
Material material;
material.albedo = AlbedoMap(material_input.albedo, texcoords);
material.normal = NormalMap(material_input.normalHeight, texcoords, tbn);
vec4 MRDAo = LightingData(material_input.MDRAo, texcoords);
material.metallic = MRDAo.r;
material.roughness = MRDAo.g;
material.dielectric = MRDAo.b;
material.ambientOcclusion = MRDAo.a;
material.emissive = EmissiveMap(material_input.emissive, texcoords);
material.F0 = Fresnel0(material.albedo, material.metallic, material.dielectric);
return material;
}
vec3 GetAllLighting(Material material, Camera camera, vec3 worldPosition, vec3 worldNormal)
{
vec3 lighting = vec3(0.0);
for(int i = 0; i < lights.length(); i++)
lighting += CalculateLight(lights[i], camera, material, worldPosition, worldNormal);
return lighting + GetAmbientLight(material.ambientOcclusion, material.albedo.rgb) + material.emissive;
}
#endif
// sah
#if defined(VERTEX_SHADER)
#define io out
#elif defined(FRAGMENT_SHADER)
#define io in
#endif
io IO
{
vec3 position;
vec3 normal;
vec3 tangent;
vec2 uv;
} sharedData;
void main(void)
{
gl_Position = (camera.projectionMatrix * camera.viewMatrix * modelMatrix) * vec4(vertex, 1.f);
sharedData.position = GetWorldNormal();
sharedData.normal = GetWorldPosition();
sharedData.tangent = GetWorldTangent(sharedData.normal);
sharedData.uv = uv;
}
