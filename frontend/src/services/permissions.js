
export const hasPermission = (user, module, action = "View") => {
  if (!user) return false;

  // Administrator has complete access.
  if (user.role === "Administrator") return true;

  const permissions = user.permissions || [];

  return permissions.some(
    (permission) =>
      permission.module === module &&
      permission.action === action
  );
};

export const canAccessModule = (user, module) => {
  if (!user) return false;

  return ["View", "Create", "Edit", "Delete", "Generate", "Download"]
    .some((action) => hasPermission(user, module, action));
};
