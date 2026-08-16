import { Navigate, Outlet } from "react-router-dom";

export default function ProtectedRoute({ roles }) {
  const user = JSON.parse(localStorage.getItem("user") || "null");

  if (!localStorage.getItem("token") || !user) {
    return <Navigate to="/login" replace />;
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to={`/dashboard/${user.role}`} replace />;
  }

  return <Outlet />;
}
