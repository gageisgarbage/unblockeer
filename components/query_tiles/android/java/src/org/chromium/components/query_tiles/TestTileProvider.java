// Copyright 2020 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

package org.chromium.components.query_tiles;

import org.chromium.base.Callback;

import java.util.ArrayList;
import java.util.List;

/**
 * Helper implementation of {@link TileProvider} for tests.
 */
public class TestTileProvider implements TileProvider {
    private List<QueryTile> mTiles = new ArrayList<>();

    /**
     * Builds and populates a {@link TileProvider} with {@code levels} tree depth and each row
     * having
     * {@code count} elements.
     * @param levels The depth of the tile tree.
     * @param count  The number of tiles in each row.
     */
    public TestTileProvider(int levels, int count) {
        mTiles = buildTiles("Tile", levels, count);
    }

    /**
     * Finds a tile by traversing the tree.
     * @param indices The indices for each child to select as the tree is traversed.
     * @return        The matching {@link QueryTile} node.
     */
    public QueryTile getTileAt(int... indices) {
        QueryTile tile = null;
        for (int index : indices) {
            List<QueryTile> tiles = tile == null ? mTiles : tile.children;
            assert index >= 0 && index < tiles.size();
            tile = tiles.get(index);
        }

        return tile;
    }

    /**
     * Finds a list of tiles at a specific row.  Passing in no arguments will give the top level
     * list. Otherwise it will traverse the tree until it finds the right tile and then return the
     * children of that tile.
     * @param indices The indices for each child to select as the tree is traversed.  No arguments
     *         is valid.
     * @return        The list of {@link QueryTile} children of a particular node.
     */
    public List<QueryTile> getChildrenOf(int... indices) {
        QueryTile tile = getTileAt(indices);
        return tile == null ? mTiles : tile.children;
    }

    // TileProvider implementation.
    @Override
    public void getQueryTiles(Callback<List<QueryTile>> callback) {
        callback.onResult(mTiles);
    }

    private static List<QueryTile> buildTiles(String prefix, int levelsLeft, int count) {
        if (levelsLeft == 0) return null;
        List<QueryTile> children = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            String id = prefix + "_" + i;
            children.add(new QueryTile(id + "_id", id + "_displayTitle", id + "_accessibilityText",
                    id + "_queryText", new String[] {id + "_url"}, null,
                    buildTiles(id, levelsLeft - 1, count)));
        }

        return children;
    }
}
