# ⚔️ BOB-Google-Maps - Strategy for Comprehensive City-Wide Extraction (Jodhpur) ⚔️

**Date:** November 18, 2025
**Performed By:** Dhrishtadyumna Coding Agent
**Objective:** To outline a strategic approach for systematically downloading data for "each and every business or location or pointer" within a defined geographic area, such as Jodhpur, Rajasthan, using the BOB-Google-Maps system.

---

## 1. Executive Summary

Achieving comprehensive, city-wide data extraction from Google Maps requires a multi-phase strategy. The BOB-Google-Maps system is designed for targeted business extraction, not broad geographical sweeps. Therefore, the primary challenge lies in **generating a comprehensive list of specific business queries** to feed into the extractor. Once this list is compiled, the system's robust batch processing and caching capabilities can efficiently execute the extraction.

---

## 2. Strategic Phases for City-Wide Extraction

### Phase A: Target Discovery & Query Generation (The Intelligence Gathering)

This is the most critical and labor-intensive phase. The goal is to create a comprehensive list of unique business names or highly specific search queries that will lead the BOB-Google-Maps extractor to individual business pages.

#### Method 1: Categorical Search (Most Effective & Practical)

This method involves systematically querying Google Maps for businesses within specific categories, combined with the target location.

1.  **Identify Broad Categories:** Start with high-level business categories relevant to the city.
    *   `restaurants in Jodhpur`
    *   `hotels in Jodhpur`
    *   `shops in Jodhpur`
    *   `hospitals in Jodhpur`
    *   `schools in Jodhpur`
    *   `banks in Jodhpur`
    *   `cafes in Jodhpur`
    *   `pharmacies in Jodhpur`
    *   `garment stores in Jodhpur`
    *   `electronics stores in Jodhpur`
    *   ... (and so on, for all relevant categories)

2.  **Refine with Sub-Categories & Localities:** For larger categories, break them down further and combine with specific localities within Jodhpur (e.g., "Sardarpura", "Shastri Nagar", "Ratanada").
    *   `North Indian restaurants in Sardarpura Jodhpur`
    *   `boutique hotels in Jodhpur old city`
    *   `sweet shops in Jodhpur`

3.  **Iterative Querying (Manual or Automated):**
    *   **Manual:** Perform these searches directly on Google Maps. As you scroll through results, Google Maps often loads more businesses. Manually collect the names of businesses that appear.
    *   **Automated (Enhancement Opportunity):** The current BOB-Google-Maps system is designed to extract *details from a known business*. It does not have a built-in "search and list" feature. An enhancement would be to develop a module that can:
        *   Perform a categorical search (e.g., "restaurants in Jodhpur").
        *   Scroll the Google Maps search results page to load all available businesses.
        *   Extract the names and basic identifying information (e.g., Place ID or direct URL) of each business from the search results.
        *   This would generate the input list for Phase B.

#### Method 2: Grid-Based Exploration (Complex, for Exhaustive Coverage)

This method is more complex and aims for exhaustive coverage by dividing the city into a grid.

1.  **Define Geographic Bounds:** Obtain the latitude/longitude coordinates for the bounding box of Jodhpur.
2.  **Generate Grid Points:** Divide this bounding box into a grid of smaller squares (e.g., 1km x 1km).
3.  **Query per Grid Point:** For each grid square's center point, perform a generic search query.
    *   `businesses near [latitude, longitude]`
    *   `shops near [latitude, longitude]`
    *   This method is prone to overlap and redundancy but can uncover businesses not easily categorized.
    *   **Automated (Enhancement Opportunity):** This would require a dedicated "grid search" module that can generate coordinates, perform searches, and extract business names from the results.

#### Method 3: Seed-Based Expansion (Enhancement Opportunity)

1.  **Start with Known Businesses:** Begin with a few known businesses in Jodhpur.
2.  **"Related Businesses" / "Businesses Nearby":** Develop a feature that, given a business's page, can extract links or names of "related businesses" or "businesses nearby" that Google Maps often suggests.
3.  **Iterative Discovery:** Recursively follow these links to discover more businesses, ensuring to track already-visited businesses to avoid loops.

### Phase B: Batch Extraction & Data Consolidation (The Execution)

Once a comprehensive list of business names/queries is generated from Phase A, the BOB-Google-Maps system can efficiently extract the detailed data.

1.  **Compile Target List:** Create a plain text file (e.g., `jodhpur_targets.txt`), with one business name or specific query per line. Ensure this list is deduplicated.
    *   Example:
        ```
        Gypsy Vegetarian Restaurant Jodhpur
        Janta Sweet House Jodhpur
        OM Cuisine Jodhpur
        Laxmi Misthan Bhandar Jodhpur
        Hotel Ratan Vilas Jodhpur
        ...
        ```

2.  **Execute Batch Extraction:** Utilize the robust `bob/utils/batch_processor.py` for reliable, parallel extraction.
    *   **Command:** 
        ```bash
        python3 bob/utils/batch_processor.py \
            --input-file jodhpur_targets.txt \
            --output jodhpur_all_businesses.json \
            --retry 1 \
            --reviews \
            --max-reviews 10
        ```
    *   **Key Features Utilized:**
        *   **`--input-file`**: Reads targets efficiently from the list.
        *   **Subprocess Isolation:** Each extraction runs in its own process, preventing memory leaks and ensuring stability for large batches.
        *   **`--retry 1`**: Provides resilience against transient network issues.
        *   **`--reviews` / `--max-reviews`**: Ensures comprehensive data capture.
        *   **`--output`**: Consolidates all results into a single JSON file.

3.  **Leverage Caching:** The `HybridExtractorOptimized` (used by the `batch_processor`) has caching enabled.
    *   If the extraction is interrupted, it can be resumed without re-scraping already processed businesses.
    *   If a business is queried multiple times (e.g., due to overlaps in discovery methods), the cached result will be returned instantly.

4.  **Data Consolidation & Deduplication:** After extraction, the `jodhpur_all_businesses.json` file will contain all the extracted data. Further processing may be required to:
    *   Deduplicate businesses (e.g., if "Janta Sweet House" was found via multiple queries). The `place_id` or `cid` fields are excellent for this.
    *   Clean and standardize data.

---

## 3. Conclusion & Next Steps

The BOB-Google-Maps system is fully capable of executing the "Phase B" (Batch Extraction) with high reliability and efficiency. The primary challenge for city-wide extraction lies in "Phase A" (Target Discovery).

**Recommendations for Comprehensive City-Wide Extraction:**

1.  **Develop a "Search & List" Module:** This is the most crucial enhancement. A new module that can perform categorical searches, scroll results, and extract business names/Place IDs would automate Phase A.
2.  **Iterative Refinement:** Start with broad categories, then refine with sub-categories and specific localities to maximize coverage.
3.  **Monitor & Adapt:** Google Maps UI changes frequently. The discovery and extraction methods will require ongoing monitoring and adaptation.

This strategy, combined with the robust capabilities of BOB-Google-Maps, provides a clear path to achieving comprehensive city-wide data extraction for Jodhpur, Rajasthan.
