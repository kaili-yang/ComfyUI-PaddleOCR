import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "PaddleOCR.PaidNodeStyle",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "PaddleOCR_Node" || nodeData.name === "PaddleOCR_Unified_Node") {
            // Override onNodeCreated to set default customized colors
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                // Set "Premium" Gold/Brown colors
                // These emulate the look of paid nodes similar to TripoSR
                this.color = "#6e570f";
                this.bgcolor = "#423308";

                return r;
            };

            // Override onDrawForeground to paint the "credits" badge
            const onDrawForeground = nodeType.prototype.onDrawForeground;
            nodeType.prototype.onDrawForeground = function (ctx) {
                const r = onDrawForeground ? onDrawForeground.apply(this, arguments) : undefined;

                if (this.flags.collapsed) return r;

                // Badge Configuration
                const text = "20 credits/Run";
                const fontSize = 12;
                const padding = 6;
                const badgeHeight = 20;

                ctx.save();
                ctx.font = `${fontSize}px sans-serif`;
                const sz = ctx.measureText(text);
                const badgeWidth = sz.width + (padding * 2);

                // Position: Top Right of the header
                // Standard Title Height is 30. We want it vertically centered in the header or near top.
                const titleHeight = LiteGraph.NODE_TITLE_HEIGHT || 30;

                const x = this.size[0] - badgeWidth - 10;
                const y = -titleHeight + 5; // Slightly down from top edge

                // Draw Badge Background
                ctx.fillStyle = "#8a6d1b"; // Lighter gold for badge
                ctx.beginPath();
                if (ctx.roundRect) {
                    ctx.roundRect(x, y, badgeWidth, badgeHeight, 4);
                } else {
                    ctx.rect(x, y, badgeWidth, badgeHeight);
                }
                ctx.fill();

                // Draw Badge Text
                ctx.fillStyle = "#ffffff";
                ctx.fillText(text, x + padding, y + badgeHeight - 5);

                ctx.restore();

                return r;
            };
        }
    },
});
