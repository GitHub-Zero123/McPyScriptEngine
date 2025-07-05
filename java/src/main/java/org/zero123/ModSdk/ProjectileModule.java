package org.zero123.ModSdk;

import com.google.gson.Gson;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.phys.Vec3;

public class ProjectileModule
{

    static class ProjectileParams
    {
        double[] position;
        double[] direction;
        float power;
        boolean isDamageOwner;
    }

    // 创建并发射抛射物
    public static String _serverShootProjectile(String entityId, String entityIdentifier, String json)
    {
        var entityOpt = EntityManager.serverGetEntityByUUID(entityId);
        if(entityOpt.isEmpty())
        {
            return "";
        }
        Gson gson = new Gson();
        ProjectileParams params = gson.fromJson(json, ProjectileParams.class);
        final var shooterId = entityOpt.get();
        Vec3 pos;
        Vec3 direction = new Vec3(0, 0, 0);
        if(params.position == null)
        {
            pos = shooterId.position();
        }
        else
        {
            pos = new Vec3(params.position[0], params.position[1], params.position[2]);
        }
        if(params.direction != null)
        {
            direction = new Vec3(params.direction[0], params.direction[1], params.direction[2]);
        }
        var shooterObj = EntityManager.createEntityByResource(shooterId.level(), entityIdentifier, pos, direction, params.power != 0 ? params.power : 1.0f);
        if(shooterObj == null)
        {
            return "";
        }
        // 不会对创建者造成伤害
        if(!params.isDamageOwner)
        {
            if(shooterObj instanceof Projectile projectile)
            {
                projectile.setOwner(shooterId);
            }
        }
        shooterId.level().addFreshEntity(shooterObj);
        return shooterObj.getUUID().toString();
    }
}
