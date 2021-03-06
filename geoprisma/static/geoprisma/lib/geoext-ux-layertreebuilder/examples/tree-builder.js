/**
 * Copyright (c) 2008-2010 The Open Source Geospatial Foundation
 * 
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

 /** api: example[tree-legend]
  *  Tree Legend
  *  -----------
  *  Render layer nodes with legends.
  */

var map, mapPanel, tree, host, url, layers;

Ext.onReady(function() {
    host = "http://dev4g.mapgears.com";
    url = host + "/cgi-bin/mswms_gmap?";
    layers = [];

    // google base layer
    layers.push(new OpenLayers.Layer.Google(
            "Google Satellite",
            {type: G_SATELLITE_MAP, sphericalMercator: true, displayInLayerSwitcher: true}
    ));

    layers.push(new OpenLayers.Layer.WMS("Canadian parks", url, {
            layers: "park",
            format: 'image/png'
        }, {
            singleTile: true,
            group: "GMap/Polygons",
            isBaseLayer: false,
            visibility: false,
            hideInLegend: true
        }
    ));

    // GMap layers
    layers.push(new OpenLayers.Layer.WMS("Canadian railroads", url, {
            layers: "rail",
            format: 'image/png'
        }, {
            singleTile: true,
            group: "GMap/Lines",
            isBaseLayer: false,
            visibility: false
        }
    ));

    layers.push(new OpenLayers.Layer.WMS("Canadian roads", url, {
            layers: "road",
            format: 'image/png'
        }, {
            singleTile: true,
            group: "GMap/Lines",
            isBaseLayer: false,
            visibility: false
        }
    ));

    layers.push(new OpenLayers.Layer.WMS("Canadian cities", url, {
            layers: "popplace",
            format: 'image/png'
        }, {
            singleTile: true,
            group: "GMap/Points",
            isBaseLayer: false,
            visibility: false
        }
    ));

    // group : Vector
    //         also shows that the "VectorLegend" is supported
    var mercator = new OpenLayers.Projection('EPSG:900913');
    var lonlat = new OpenLayers.Projection('EPSG:4326');
        
    var features = new Array(50);
    for (var i=0; i<features.length; i++) {
        features[i] = new OpenLayers.Feature.Vector(
            new OpenLayers.Geometry.Point(
                (20 * Math.random()) - 80, 20 * Math.random() + 40
            ).transform(lonlat, mercator)
        );
    }
    var rules = [
        new OpenLayers.Rule({
            title: "Blue stars",
            symbolizer: {
                graphicName: "star",
                pointRadius: 8,
                fillColor: "#99ccff",
                strokeColor: "#666666",
                strokeWidth: 1
            }
        })
    ];
    var vector = new OpenLayers.Layer.Vector('Vector points', {
        styleMap: new OpenLayers.StyleMap(
            new OpenLayers.Style({}, {rules: rules})
        ),
        visibility: false,
        group: "Vector"
    });
    vector.addFeatures(features);
    layers.push(vector);

    // group : undefined
    layers.push(new OpenLayers.Layer.Vector(
        "Layer without any group is classified as 'other layer'",
        {visibility: false}
    ));

    // a base layer without any group is added to the 'base layer' group
    layers.push(new OpenLayers.Layer.Google("Google Street",
        {sphericalMercator: true, visibility: false}
    ));

    // a base layer with a group is added to the group instead of the 
    // 'base layer' group
    layers.push(new OpenLayers.Layer.WMS("Canada bathymetry", url, {
            layers: "base",
            format: 'image/png'
        }, {
            singleTile: true,
            visibility: false,
            group: "GMap/Base"
        }
    ));

    // a layer with 'displayInLayerSwitcher': false shouldn't be added to the
    // layertree... and shouldn't have a group (if it has any, it should be
    // removed...)
    layers.push(new OpenLayers.Layer.WMS("displayInLayerSwitcher:false", url, {
            layers: "park",
            format: 'image/png'
        }, {
            singleTile: true,
            group: "GMap/Polygons",
            isBaseLayer: false,
            visibility: false,
            displayInLayerSwitcher: false
        }
    ));

    map = new OpenLayers.Map({
        projection: new OpenLayers.Projection("EPSG:900913"),
        units: "m",
        numZoomLevels: 18,
        maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(-20037508, -20037508,
                                         20037508, 20037508.34)
    });

    mapPanel = new GeoExt.MapPanel({
        region: "center",
        center: [-7924121.1710935, 6185868.5449234],
        zoom: 10,
        map: map
    });

    map.addLayers(layers);

    tree = new GeoExt.ux.tree.LayerTreeBuilder({
        region: "east",
        width: 250,
        autoScroll: true,
        rootVisible: false,
        lines: false,
        // widget custom properties
        wmsLegendNodes: true,
        vectorLegendNodes: true
    });

    new Ext.Viewport({
        layout: "fit",
        hideBorders: true,
        items: {
            layout: "border",
            items: [
                mapPanel, tree, {
                    contentEl: desc,
                    region: "west",
                    width: 250,
                    bodyStyle: {padding: "5px"}
                }
            ]
        }
    });

    map.setCenter(new OpenLayers.LonLat(-7924121.1710935, 6185868.5449234), 6);
});
