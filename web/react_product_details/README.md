# React Native Product Details Test

This project is a small technical test built with **React Native
(Expo)**. Its purpose is to demonstrate basic understanding of component
structure, props usage, state handling, and layout styling in a mobile
environment.

## Overview

The application renders a single screen: a **Product Details** view.

All product data is passed as a JSON object via props, simulating how a
real application would receive data from an API.

There is **no navigation, backend integration, or persistence**. This is
intentionally a minimal, self-contained example focused only on UI and
state behavior.

## Component Structure

Everything is implemented inside a single component to keep the example
simple.

### ProductDetails

Receives a `product` object via props and renders the interface.

The product JSON includes:

-   `name` -- Product title
-   `price` -- Unit price
-   `rating` -- Rating value
-   `calories` -- Nutritional info (mock data)
-   `time` -- Preparation time (mock data)
-   `description` -- Product description
-   `image` -- Image URL

This simulates the structure of a real API response.

## State Management

Two local states are used with `useState`:

-   `qty` → Controls the selected quantity
-   `fav` → Toggles the favorite icon

These states trigger automatic UI updates when changed, demonstrating
React's reactive rendering model.

## Layout Sections

The screen is visually divided into:

1.  **Header**
    -   Back button (visual only)
    -   Title
    -   Favorite toggle
2.  **Product Highlight**
    -   Gradient background container
    -   Product name and image
3.  **Quantity Selector**
    -   Increment / decrement controls
    -   Dynamic price calculation
4.  **Info Row**
    -   Rating, calories, and preparation time
5.  **Description**
    -   Static explanatory text
6.  **Actions**
    -   "Add to Cart" button (outlined)
    -   "Buy Now" button (highlighted)

## Notes

This is not a production-ready structure.

Because this is only a test: - No modularization was applied - No
styling separation (e.g., StyleSheet files) - No navigation or state
libraries - No API calls - No business logic layer

The goal was to keep everything visible in one place to clearly
demonstrate how props, state, and layout interact in React Native.
