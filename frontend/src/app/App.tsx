import { useEffect, useState } from "react";

import CampaignWorkspace from "../pages/campaigns/CampaignWorkspace";
import ProductCardWorkspace from "../pages/products/ProductCardWorkspace";

type WorkspaceRoute = "products" | "campaigns";

function resolveWorkspaceRoute(): WorkspaceRoute {
  const path = window.location.pathname.toLowerCase();
  const hash = window.location.hash.toLowerCase();

  if (hash === "#campaigns") {
    return "campaigns";
  }

  if (hash === "#products") {
    return "products";
  }

  if (path.endsWith("/campaigns")) {
    return "campaigns";
  }

  return "products";
}

function App() {
  const [workspaceRoute, setWorkspaceRoute] =
    useState<WorkspaceRoute>(resolveWorkspaceRoute);

  useEffect(() => {
    function syncWorkspaceRoute() {
      setWorkspaceRoute(resolveWorkspaceRoute());
    }

    window.addEventListener("hashchange", syncWorkspaceRoute);
    window.addEventListener("popstate", syncWorkspaceRoute);

    return () => {
      window.removeEventListener("hashchange", syncWorkspaceRoute);
      window.removeEventListener("popstate", syncWorkspaceRoute);
    };
  }, []);

  if (workspaceRoute === "campaigns") {
    return <CampaignWorkspace />;
  }

  return <ProductCardWorkspace />;
}

export default App;
