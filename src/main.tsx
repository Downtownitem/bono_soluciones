import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider, } from "react-router-dom";
import { NextUIProvider } from "@nextui-org/react"

import "./index.css";

import App from "./App";

const container = document.getElementById("root");
if (!container) throw new Error("Could not find root element with id 'root'");

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />
  }
]);

ReactDOM.createRoot(container).render(
  <React.StrictMode>
    <NextUIProvider>
      <RouterProvider router={router} />
    </NextUIProvider>
  </React.StrictMode>
);