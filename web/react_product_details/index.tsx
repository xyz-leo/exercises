import React, { useState } from "react";
import { View, Text, Image, TouchableOpacity } from "react-native";
import { LinearGradient } from "expo-linear-gradient";

function ProductDetails({ product }) {
  const [qty, setQty] = useState(1);
  const [fav, setFav] = useState(false);

  const inc = () => setQty(qty + 1);
  const dec = () => qty > 1 && setQty(qty - 1);

  return (
    <View style={{ margin: 20, padding: 20, borderRadius: 16, backgroundColor: "#f7f7f7", elevation: 3 }}>
      
      {/* HEADER */}
      <View style={{ justifyContent: "center", marginBottom: 10 }}>
        <TouchableOpacity
          onPress={() => console.log("Back")}
          style={{ position: "absolute", left: 0, paddingHorizontal: 12, paddingVertical: 6, backgroundColor: "#fff", borderRadius: 12, elevation: 3 }}
        >
          <Text style={{ fontSize: 18 }}>{"<"}</Text>
        </TouchableOpacity>

        <Text style={{ fontSize: 18, fontWeight: "bold", textAlign: "center" }}>
          Product Details
        </Text>

        <TouchableOpacity
          onPress={() => setFav(!fav)}
          style={{ position: "absolute", right: 0 }}
        >
          <Text style={{ fontSize: 20 }}>{fav ? "❤️" : "🤍"}</Text>
        </TouchableOpacity>
      </View>

      {/* IMAGE + TITLE */}
      <LinearGradient
        colors={["#FFE8A3", "#FFF1C9", "#FFF6DD"]}
        style={{ padding: 15, borderRadius: 16 }}
      >
        <Text style={{ fontSize: 20, fontWeight: "bold" }}>{product.name}</Text>

        <Image
          source={{ uri: product.image }}
          style={{ height: 180, borderRadius: 12, marginTop: 10 }}
        />
      </LinearGradient>

      {/* QUANTITY + PRICE */}
      <View style={{ flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginTop: 20 }}>
        
        <View style={{ flexDirection: "row", alignItems: "center", backgroundColor: "#F2C94C", borderRadius: 22, paddingHorizontal: 10, paddingVertical: 6 }}>
          <TouchableOpacity onPress={dec}>
            <Text style={{ fontSize: 18, fontWeight: "bold" }}>−</Text>
          </TouchableOpacity>

          <Text style={{ fontSize: 18, fontWeight: "600", marginHorizontal: 10 }}>
            {qty}
          </Text>

          <TouchableOpacity onPress={inc}>
            <Text style={{ fontSize: 18, fontWeight: "bold" }}>+</Text>
          </TouchableOpacity>
        </View>

        <Text style={{ fontSize: 20, fontWeight: "bold" }}>
          R$ {(product.price * qty).toFixed(2)}
        </Text>
      </View>

      {/* INFO ROW */}
      <View style={{ flexDirection: "row", justifyContent: "space-between", marginTop: 20 }}>
        <Text>⭐ {product.rating}</Text>
        <Text>🔥 {product.calories} Calories</Text>
        <Text>⏱️ {product.time} min</Text>
      </View>

      {/* DESCRIPTION */}
      <Text style={{ marginTop: 20, fontSize: 20, fontWeight: "bold" }}>
        Description
      </Text>

      <Text style={{ marginTop: 10, color: "#555" }}>
        {product.description}
      </Text>

      {/* ACTION BUTTONS */}
      <View style={{ flexDirection: "row", marginTop: 25, gap: 12 }}>
        
        <TouchableOpacity
          style={{ flex: 1, backgroundColor: "#fff", borderWidth: 2, borderColor: "#F2C94C", paddingVertical: 14, borderRadius: 16, alignItems: "center" }}
        >
          <Text style={{ fontSize: 16, fontWeight: "600", color: "#C59B2A" }}>
            Add to Cart
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={{ flex: 1, backgroundColor: "#F2C94C", paddingVertical: 14, borderRadius: 16, alignItems: "center", elevation: 4 }}
        >
          <Text style={{ fontSize: 16, fontWeight: "700", color: "#333" }}>
            Buy Now
          </Text>
        </TouchableOpacity>

      </View>
    </View>
  );
}

export default function Index() {
  const product = {
    name: "Blueberry and Raspberry Pancakes",
    price: 25,
    rating: "5.0",
    calories: 450,
    time: "15-25",
    description:
      "This vibrant and fruity addition brings a burst of flavor and color to your morning stack, making every bite a celebration of fresh, juicy berries.",
    image:
      "https://static.vecteezy.com/system/resources/previews/008/601/556/non_2x/flat-pancake-animation-cartoon-with-blueberry-and-strawberry-illustration-image-vector.jpg"
  };

  return <ProductDetails product={product} />;
}
