import { useEffect, useState } from "react";

import CampaignWorkspace from "../pages/campaigns/CampaignWorkspace";
import KnowledgeWorkspace from "../pages/knowledge/KnowledgeWorkspace";
import ProductCardWorkspace from "../pages/products/ProductCardWorkspace";

type WorkspaceRoute = "knowledge" | "products" | "campaigns";

function resolveWorkspaceRoute(): WorkspaceRoute {
  const path = window.location.pathname.toLowerCase();
  const hash = window.location.hash.toLowerCase();

  if (hash === "#knowledge") {
    return "knowledge";
  }

  if (hash === "#campaigns") {
    return "campaigns";
  }

  if (hash === "#products") {
    return "products";
  }

  if (path.endsWith("/campaigns")) {
    return "campaigns";
  }

  if (path.endsWith("/knowledge")) {
    return "knowledge";
  }

  return "knowledge";
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

  if (workspaceRoute === "knowledge") {
    return <KnowledgeWorkspace />;
  }

  return <ProductCardWorkspace />;
}

export default App;
