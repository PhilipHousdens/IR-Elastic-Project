<script lang="ts">

</script>
<template>
    <div class=" w-full h-16 bg-amber-400 flex items-center justify-between px-10">
        <div>
            <p class="text-2xl">Food<b class="text-white">YUMYUM</b></p>
        </div>
        <div class="space-x-4 text-lg">
            <router-link to="/">Home</router-link>
            <router-link to="/">Folder</router-link>
            <router-link to="/">Bookmark</router-link>
            <router-link to="/">Recommendation</router-link>
        </div>
        <div>
            <div class="flex space-x-4">
                <div class="bg-white px-3 py-2 rounded-3xl">
                    <p>
                        Sign In
                    </p>
                </div>
                <div class="bg-white px-3 py-2 rounded-3xl">
                    <p>
                        Sign up
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>